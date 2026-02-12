#!/usr/bin/env pypy3

import shutil
import subprocess
import string
import zipfile
import tempfile
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import os
import re
import math
import random
import multiprocessing
import copy
from collections import Counter
import traceback
from ast import literal_eval
import signal
from dataclasses import dataclass, field, fields
import statistics
import sys
from itertools import permutations

@dataclass(slots=True)
class Score:
	effort: int = 0
	sfb: int = 0
	rolling: int = 0
	scissors: int = 0

@dataclass(slots=True)
class Layout:
	letters: list[list[str]]
	score: Score = field(default_factory=lambda: Score())
	total: int = 0
	left_usage: int = 0
	right_usage: int = 0
	source: str = "random"

	def clone(self):
		return Layout(
			[row[:] for row in self.letters],
			source=self.source,
		)

	def __post_init__(self):
		self.letters = [r[:] for r in self.letters]
		self.calc_scores()
		if SCORE_MEDIAN is not None:
			self.calc_total_score()

	def __eq__(self, other):
		if not isinstance(other, Layout):
			return False
		return self.letters == other.letters

	def __hash__(self):
		return hash(tuple(tuple(r) for r in self.letters))

	def calc_scores(self):
		_effort_grid = EFFORT_GRID
		_bigrams = BIGRAMS
		_trigrams = TRIGRAMS
		_bigram_score_table = BIGRAM_SCORE_TABLE
		_trigram_score_table = TRIGRAM_SCORE_TABLE
		pos = {}

		sfb = 0
		rolling = 0
		scissors = 0

		self.score = Score()
		self.left_usage = 0
		self.right_usage = 0

		for r in range(ROWS):
			for c in range(COLS):
				ch = self.letters[r][c]
				if ch != ' ':
					pos[ch] = (r*COLS) + c
					try:
						l = LETTERS[ch]
					except KeyError:
						print('======= ERROR')
						print_layout(self)
						sys.exit(1)
					self.score.effort += l * _effort_grid[r][c]
					if c < 5:
						self.left_usage += l
					else:
						self.right_usage += l

		for pair, count in _bigrams.items():
			a, b = pair[0], pair[1]

			if a not in pos or b not in pos:
				continue

			i = pos[a]
			j = pos[b]
			target_score = _bigram_score_table[i][j]
			sfb += count * target_score.sfb
			rolling += count * target_score.rolling
			scissors += count * target_score.scissors

		for pair, count in _trigrams.items():
			a, b, c = pair[0], pair[1], pair[2]

			if a not in pos or b not in pos or c not in pos:
				continue

			i = pos[a]
			j = pos[b]
			k = pos[c]
			target_score = _trigram_score_table[i][j][k]
			sfb += count * target_score.sfb
			rolling += count * target_score.rolling
			scissors += count * target_score.scissors

		self.score.sfb = sfb
		self.score.rolling = rolling
		self.score.scissors = scissors

	def calc_total_score(self):
		def norm(v, m, d):
			return (v - m) / d

		r = Score(
			effort=norm(self.score.effort, SCORE_MEDIAN.effort, SCORE_SCALE.effort),
			sfb=norm(self.score.sfb, SCORE_MEDIAN.sfb, SCORE_SCALE.sfb),
			rolling=norm(self.score.rolling, SCORE_MEDIAN.rolling, SCORE_SCALE.rolling),
			scissors=norm(self.score.scissors, SCORE_MEDIAN.scissors, SCORE_SCALE.scissors),
		)

		self.total = int(
			(-r.effort) * SCORE_RATES.effort +
			(-r.sfb) * SCORE_RATES.sfb +
			(r.rolling) * SCORE_RATES.rolling +
			(-r.scissors) * SCORE_RATES.scissors
		)

TMP_PATH = None
ANALYZE_RESULT_FILENAME = 'analyze_result.tsv'
RESULT_FILENAME = 'result.txt'

LETTERS = Counter()
BIGRAMS = Counter()
TRIGRAMS = Counter()

ROWS = 3
COLS = 10
EFFORT_GRID = [
	[3.2, 2.4, 2.0, 2.2, 10.0, 10.0, 5.2, 5.0, 5.4, 6.2],
	[1.5, 1.3, 1.1, 1.0,  3.5,  6.5, 4.0, 4.1, 4.3, 4.5],
	[3.0, 2.6, 2.3, 1.6, 10.0, 10.0, 4.6, 5.3, 5.6, 6.0],
]

FINGER_GRID = [
	[4, 3, 2, 1, 1, 1, 1, 2, 3, 4],
	[4, 3, 2, 1, 1, 1, 1, 2, 3, 4],
	[4, 3, 2, 1, 1, 1, 1, 2, 3, 4],
]

SCORE_RATES = Score(
	sfb = 0.50,
	effort = 0.30,
	rolling = 0.15,
	scissors = 0.05,
)
SCORE_MEDIAN = None
SCORE_SCALE = None

BIGRAM_SCORE_TABLE = None
TRIGRAM_SCORE_TABLE = None

EXT_TEXT = {
	'.md', '.markdown',
	'.txt', '.text',
	'.rst',
	'.adoc', '.asciidoc', '.asc',
	'.org',
	'.tex',
	'.LICENSE', 'LICENSE',
	'readme', 'README',
	'.html', '.htm',
	'.json',
	'.fxml', '.xml', '.svg', '.vue',
}

EXT_C_STYLE = {
	'.c', '.h',
	'.cpp', '.hpp', '.cc', '.hh',
	'.cxx', '.hxx',
	'.dts', '.dtsi',
	'.ino',
	'.cs',
	'.java',
	'.kt', '.kts',
	'.scala',
	'.go',
	'.rs',
	'.zig',
	'.js', '.jsx', '.mjs',
	'.ts', '.tsx',
	'.swift',
	'.m', '.mm',
	'.php',
	'.groovy',
	'.gradle',
	'.css', '.scss', '.less',
	'.v', '.sv',
	'.dart', '.sol', '.proto',
}

EXT_SCRIPT_STYLE = {
	'.py',
	'.rb',
	'.sh', '.bash', '.zsh', '.fish',
	'.conf', '.ini', '.cfg',
	'.gitconfig', '.gitignore',
	'.pl', '.pm',
	'.R', '.r',
	'.jl',
	'.ex', '.exs',
	'.yaml', '.yml', '.toml',
	'.dockerfile', 'Dockerfile',
	'Makefile', '.mk', '.make',
	'.cmake',
}

EXT_DASH_STYLE = {
	'.sql',
	'.lua',
	'.hs', '.lhs',
	'.vhd', '.vhdl',
	'.elm',
	'.ada', '.adb', '.ads',
}

EXT_PERCENT_STYLE = {
	'.erl', '.hrl',
}

EXT_SEMI_STYLE = {
	'.asm', '.s', '.S',
	'.clj', '.cljs', '.cljc', '.edn',
	'.lisp', '.lsp', '.scm',
	'.ini',
}

EXT_PAREN_STAR_STYLE = {
	'.ml', '.mli',
	'.fs', '.fsi', '.fsx',
	'.pas', '.pp',
}

def layout_key(l):
	return (
		l.total,
		l.left_usage,
		-l.score.sfb,
		-l.score.effort,
		l.score.rolling,
		-l.score.scissors,
	)

def best_layout(layouts: list[Layout]):
	return max(layouts, key=layout_key).clone()

def sort_layouts(layouts: list[Layout]):
	layouts.sort(key=layout_key, reverse=True)
	return layouts

def sort_unique_layouts(layouts: list[Layout], size):
	layouts = sort_layouts(list(set(layouts)))
	result = []

	for layout in layouts:
		if len(result) == size:
			break
		a = flatten(layout.letters)
		is_unique = True
		for l in result:
			if layout == l or \
					20 < sum(1 for c1, c2 in zip(a, flatten(l.letters)) if c1 == c2):
				is_unique = False
				break

		if is_unique:
			result.append(layout)

	return result

def init_score_state():
	global SCORE_MEDIAN, SCORE_SCALE, BIGRAM_SCORE_TABLE, TRIGRAM_SCORE_TABLE
	_effort_grid = EFFORT_GRID
	_finger_grid = FINGER_GRID
	num_keys = ROWS*COLS
	max_e = max(val for row in _effort_grid for val in row if val < 10.0)
	half = COLS/2

	BIGRAM_SCORE_TABLE = [[Score() for _ in range(num_keys)] for _ in range(num_keys)]
	for i in range(num_keys):
		for j in range(num_keys):
			self = BIGRAM_SCORE_TABLE[i][j]
			r1, c1 = divmod(i, COLS)
			r2, c2 = divmod(j, COLS)
			f1 = _finger_grid[r1][c1]
			f2 = _finger_grid[r2][c2]
			e1 = _effort_grid[r1][c1]
			e2 = _effort_grid[r2][c2]
			row_delta = abs(r1 - r2)
			is_center = (4<=c1<=5 or 4<=c2<=5)

			# sfb
			if f1 == f2:
				weight = 2.0 if is_center else 1.0
				weight *= (1.2 ** row_delta)
				self.sfb = weight * (e1+e2)
			else:
				has_gap = abs(f1-f2) > 1
				is_switching = (c1<=4 and 5<=c2)

				# scissors
				if is_center or (not has_gap and row_delta == 2) :
					self.scissors = (e1+e2)
				else: # rolling
					weight = 0.5 if is_switching else 1.0
					weight *= (0.7 ** has_gap)
					weight *= (0.8 ** row_delta)
					if f2 > f1: # outroll
						weight *= 0.5
					self.rolling = weight * (max_e*2 - (e1+e2))

	TRIGRAM_SCORE_TABLE = [[[Score() for _ in range(num_keys)] for _ in range(num_keys)] for _ in range(num_keys)]
	for i in range(num_keys):
		for j in range(num_keys):
			for k in range(num_keys):
				self = TRIGRAM_SCORE_TABLE[i][j][k]
				r1, c1 = divmod(i, COLS)
				r2, c2 = divmod(j, COLS)
				r3, c3 = divmod(k, COLS)
				f1 = _finger_grid[r1][c1]
				f2 = _finger_grid[r2][c2]
				f3 = _finger_grid[r3][c3]
				e1 = _effort_grid[r1][c1]
				e2 = _effort_grid[r2][c2]
				e3 = _effort_grid[r3][c3]

				# sfb
				sfb1 = (f1 == f2)
				sfb2 = (f2 == f3)
				if sfb1 or sfb2:
					if sfb1:
						weight = 2.0 if (4<=c1<=5 or 4<=c2<=5) else 1.0
						weight *= (1.2 ** abs(r1-r2))
						self.sfb += 0.5 * weight * (e1+e2)
					if sfb2:
						weight = 2.0 if (4<=c2<=5 or 4<=c3<=5) else 1.0
						weight *= (1.2 ** abs(r2-r3))
						self.sfb += 0.5 * weight * (e2+e3)
				# sfs
				elif f1 == f3:
					weight = 2.0 if (4<=c1<=5 or 4<=c3<=5) else 1.0
					weight *= (1.2 ** abs(r1-r3))
					self.sfb += weight * (e1+e3)
				else:
					is_center1 = (4<=c1<=5 or 4<=c2<=5)
					is_center2 = (4<=c2<=5 or 4<=c3<=5)
					row_delta1 = abs(r1 - r2)
					row_delta2 = abs(r2 - r3)
					row_delta_sum = row_delta1 + row_delta2
					has_gap1 = abs(f1 - f2) > 1
					has_gap2 = abs(f2 - f3) > 1
					has_gap_sum = has_gap1 + has_gap2
					is_switching = (c1<=4 and 5<=c2) or (c2<=4 and 5<=c3)

					# scissors
					scissors1 = is_center1 or (not has_gap1 and row_delta1 == 2)
					scissors2 = is_center2 or (not has_gap2 and row_delta2 == 2)
					if scissors1 or scissors2:
						if scissors1:
							self.scissors += 0.5 * (e1+e2)
						if scissors2:
							self.scissors += 0.5 * (e2+e3)
					else: # rolling
						if (f3 < f2 < f1): # inroll
							weight = 0.5 if is_switching else 1.0
						elif (f3 > f2 > f1): # outroll
							weight = 0.25 if is_switching else 0.5
						else: # redirect
							weight = -1.0

						if weight > 0:
							s = 1
							e = (max_e*3 - (e1+e2+e3))
						else:
							s = -1
							e = e1+e2+e3
						weight *= 0.7 ** (s * has_gap_sum)
						weight *= 0.8 ** (s * row_delta_sum)
						self.rolling = weight * e

	def iqr(v):
		q = statistics.quantiles(v, n=4, method="inclusive")
		return q[2] - q[0]

	base_layout = make_initial_layout()
	unique_layouts = {base_layout.clone()}
	while len(unique_layouts) < 100:
		unique_layouts.add(make_random(base_layout))
	layouts = list(unique_layouts)

	vals = {f.name: [getattr(l.score, f.name) for l in layouts] for f in fields(Score)}

	med_map = {}
	iqr_map = {}
	for k, v in vals.items():
		d = iqr(v)
		med = statistics.median(v)
		if d == 0:
			d = max(abs(med), 1) * 1e-9

		iqr_map[k] = d
		med_map[k] = med

	SCORE_SCALE = Score(**iqr_map)
	SCORE_MEDIAN = Score(**med_map)

def check_target_url(url):
	try:
		req = urllib.request.Request(url, method='HEAD')
		with urllib.request.urlopen(req, timeout=5) as res:
			if res.status == 200: return True
	except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout): pass

	return False

def download_target(url, dest):
	repo_name = url.rstrip('/').split('/')[-1]
	base_url = url.rstrip('/') + '/zipball/HEAD'
	suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
	target_dir = os.path.join(dest, f"{repo_name}_{suffix}")
	os.makedirs(target_dir, exist_ok=True)

	try:
		z = os.path.join(target_dir, f'{repo_name}.zip')
		subprocess.run(
			[
				'curl', '-L', '-f', '-s',
				'--connect-timeout', '30',
				'--retry', '3',
				'--retry-delay', '2',
				'-o', z, base_url
			],
			check=True, capture_output=True
		)

		if zipfile.is_zipfile(z):
			with zipfile.ZipFile(z, 'r') as zz:
				zz.extractall(target_dir)
	except Exception as e:
		print(e)
		os.remove(z)
		return False

	os.remove(z)
	return True

def cleanup(sig, frame):
	global TMP_PATH
	try:
		if TMP_PATH and os.path.exists(TMP_PATH):
			shutil.rmtree(TMP_PATH)
	except Exception:
		pass
	sys.exit(1)

def save_analyze_result(result_path):
	file_path = os.path.join(result_path, ANALYZE_RESULT_FILENAME)

	with open(file_path, 'w', encoding='utf-8') as f:
		f.write('letter\tfrequency\n')
		for ch, count in LETTERS.most_common():
			f.write(f'{ch}\t{count}\n')

		f.write('\nbigram\tfrequency\n')
		for bg, count in BIGRAMS.most_common():
			f.write(f'{bg}\t{count}\n')

		f.write('\ntrigram\tfrequency\n')
		for tg, count in TRIGRAMS.most_common():
			f.write(f'{tg}\t{count}\n')

def load_analysis_result(result_path):
	global LETTERS, BIGRAMS, TRIGRAMS 

	file_path = os.path.join(result_path, ANALYZE_RESULT_FILENAME)

	with open(file_path, 'r', encoding='utf-8') as f:
		section = None
		for line in f:
			line = line.strip()
			if not line:
				continue
			if line.startswith('letter\t'):
				section = 'letters'
				continue
			elif line.startswith('bigram\t'):
				section = 'bigrams'
				continue
			elif line.startswith('trigram\t'):
				section = 'trigrams'
				continue

			if section == 'letters':
				ch, count = line.split('\t')
				LETTERS[ch] = int(count)
			elif section == 'bigrams':
				bg, count = line.split('\t')
				BIGRAMS[bg] = int(count)
			elif section == 'trigrams':
				tg, count = line.split('\t')
				TRIGRAMS[tg] = int(count)

def analyze_target_single(full_path):
	letters = Counter()
	bigrams = Counter()
	trigrams = Counter()
	pattern = re.compile('[a-z]+', re.IGNORECASE)
	try:
		with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
			text = get_text_content(full_path, f.read())
			if not text.strip():
				pass
			groups = pattern.findall(text)
			for g in groups:
				word = g.lower()
				word = [ch for ch in word if 'a' <= ch <= 'z']
				for ch in word:
					letters[ch] += 1
				for i in range(len(word)-1):
					if word[i] != word[i+1]:
						bigrams[word[i] + word[i+1]] += 1
				for i in range(len(word)-2):
					trigrams[word[i] + word[i+1] + word[i+2]] += 1
	except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
		print(f'Failed: {full_path} — {e}')

	return letters, bigrams, trigrams

def analyze_target(result_path):
	global LETTERS, BIGRAMS, TRIGRAMS, TMP_PATH

	targets = [
		'https://github.com/torvalds/linux',            # C
		'https://github.com/opencv/opencv',             # C++
		'https://github.com/gcc-mirror/gcc',            # C++
		'https://github.com/llvm/llvm-project',         # C++/C
		'https://github.com/python/cpython',            # C/Python
		'https://github.com/numpy/numpy',               # Python/C
		'https://github.com/django/django',             # Python
		'https://github.com/psf/requests',              # Python
		'https://github.com/facebook/react',            # JavaScript/TypeScript
		'https://github.com/reactjs/react.dev',
		'https://github.com/microsoft/vscode',          # TypeScript
		'https://github.com/sveltejs/svelte',           # JavaScript/TypeScript
		'https://github.com/nodejs/node',               # JavaScript/C++
		'https://github.com/denoland/deno',             # TypeScript/Rust
		'https://github.com/kubernetes/kubernetes',     # Go
		'https://github.com/golang/go',                 # Go
		'https://github.com/rust-lang/rust',            # Rust
		'https://github.com/rust-lang/book',            # Rust
		'https://github.com/rust-lang/cargo',            # Rust
		'https://github.com/rust-lang/rfcs',            # Rust
		'https://github.com/theseus-os/Theseus',        # Rust
		'https://github.com/bytecodealliance/wasmtime', # Rust
		'https://github.com/sharkdp/fd',                # Rust
		'https://github.com/ziglang/zig',               # Zig
		'https://github.com/vlang/v',                   # V
		'https://github.com/nim-lang/Nim',              # Nim
		'https://github.com/carbon-language/carbon-lang', # Carbon
		'https://github.com/ValeLang/Vale',             # Vale
		'https://github.com/rails/rails',               # Ruby
		'https://github.com/elixir-lang/elixir',        # Elixir
		'https://github.com/apple/swift',               # Swift
		'https://github.com/JetBrains/kotlin',          # Kotlin
		'https://github.com/php/php-src',               # PHP
		'https://github.com/lua/lua',                   # Lua
		'https://github.com/ghc/ghc',                   # Haskell
		'https://github.com/scala/scala',               # Scala
		'https://github.com/wch/r-source',              # R
		'https://github.com/dotnet/runtime',            # C#
		'https://github.com/openjdk/jdk',               # Java
		'https://github.com/ohmyzsh/ohmyzsh',           # Shell
		'https://github.com/copy/v86',                  # Assembly/JavaScript
		'https://github.com/cirosantilli/x86-bare-metal-examples', # Assembly/C
		'https://github.com/mit-pdos/xv6-public',       # C/Assembly
		'https://github.com/redox-os/redox',            # Rust/Assembly
		'https://github.com/SerenityOS/serenity',       # C++/Assembly
		'https://github.com/u-boot/u-boot',             # C/Assembly
		'https://github.com/coreboot/coreboot',         # C/Assembly
		'https://github.com/Maratyszcza/PeachPy',       # Python/Assembly
		'https://github.com/netwide-assembler/nasm',    # Assembly
		'https://github.com/BeaEngine/BeaEngine',       # Assembly/C
		'https://github.com/ApolloTeam-dev/AROS',       # C/Assembly
		'https://github.com/mdn/content',
		'https://github.com/progit/progit2',
		'https://github.com/tldr-pages/tldr',
		'https://github.com/docker/docs',
		'https://github.com/pytorch/examples',
		'https://github.com/GITenberg/Moby-Dick--Or-The-Whale_2701',
		'https://github.com/GITenberg/The-Adventures-of-Sherlock-Holmes_1661',
		'https://github.com/GITenberg/The-Great-Gatsby_64317',
		'https://github.com/GITenberg/Alice-s-Adventures-in-Wonderland_11',
	]

	EXTENSIONS = EXT_TEXT | EXT_C_STYLE | EXT_SCRIPT_STYLE | EXT_DASH_STYLE | EXT_PERCENT_STYLE | EXT_SEMI_STYLE | EXT_PAREN_STAR_STYLE

	# Download
	len_targets = len(targets)
	TMP_PATH = tempfile.mkdtemp(dir=os.path.expanduser('~'), prefix='keeb')
	print('[Download Target]')
	downloaded = 0
	for url in targets:
		if download_target(url, TMP_PATH):
			downloaded += 1
			print(f'\r\033[K{downloaded}/{len_targets} ({downloaded/len_targets*100:.1f}%)', end='')
		else:
			print(f'Failed {url}')
	print(f'\r\033[K...Done')

	# file list
	files = []
	for root, dirs, fs in os.walk(TMP_PATH):
		for file in fs:
			name, ext = os.path.splitext(file)
			if ext.lower() in EXTENSIONS or name.lower() == 'readme':
				files.append(os.path.join(root, file))

	# Calc LETTERS, BIGRAMS
	print('[Analyze Target]')
	letters = Counter()
	bigrams = Counter()
	trigrams = Counter()
	symbols = Counter()
	symbol_bigrams = Counter()
	len_files = len(files)
	with ProcessPoolExecutor() as executor:
		for i, (l, b, t) in enumerate(executor.map(analyze_target_single, files), 1):
			letters += l
			bigrams += b
			trigrams += t
			print(f'\r\033[K{i}/{len_files} ({i/len_files*100:.1f}%)', end='')

	LETTERS = letters

	total_count = sum(bigrams.values())
	threshold = total_count * 0.99
	cumulative = 0
	for bigram, count in bigrams.most_common():
		cumulative += count
		BIGRAMS[bigram] = count
		if cumulative >= threshold:
			break

	total_count = sum(trigrams.values())
	threshold = total_count * 0.9
	cumulative = 0
	for trigram, count in trigrams.most_common():
		cumulative += count
		TRIGRAMS[trigram] = count
		if cumulative >= threshold:
			break

	shutil.rmtree(TMP_PATH)
	print(f'\r\033[K...Done')

	# Store result
	save_analyze_result(result_path)

def get_text_content(full_path, original_text):
	filename = os.path.basename(full_path)
	name, ext = os.path.splitext(full_path)
	ext = ext.lower()

	if ext in EXT_TEXT or name.lower() == 'readme':
		return original_text

	comments = []

	if ext in EXT_C_STYLE:
		comments.extend(re.findall(r'/\*[\s\S]*?\*/', original_text))
		comments.extend(re.findall(r'//.*', original_text))
	elif ext in EXT_SCRIPT_STYLE:
		if ext == '.py':
			comments.extend(re.findall(r'"{3}[\s\S]*?"{3}', original_text))
			comments.extend(re.findall(r"'{3}[\s\S]*?'{3}", original_text))
		comments.extend(re.findall(r'#.*', original_text))
	elif ext in EXT_DASH_STYLE:
		if ext == '.hs':
			comments.extend(re.findall(r'\{-[\s\S]*?-\}', original_text))
		elif ext == '.lua':
			comments.extend(re.findall(r'--\[\[[\s\S]*?\]\]', original_text))
		comments.extend(re.findall(r'--.*', original_text))
	elif ext in EXT_PERCENT_STYLE:
		comments.extend(re.findall(r'%.*', original_text))
	elif ext in EXT_SEMI_STYLE:
		comments.extend(re.findall(r';.*', original_text))
	elif ext in EXT_PAREN_STAR_STYLE:
		comments.extend(re.findall(r'\(\*[\s\S]*?\*\)', original_text))
	else:
		return ""

	return "\n".join(comments)

def make_initial_layout() -> Layout:
	grid = [] 
	coords = []
	for r in range(3):
		for c in range(10):
			coords.append((EFFORT_GRID[r][c], r, c))
	coords.sort()

	letters_sorted = [ch for ch, _ in LETTERS.most_common()]
	layout = [[' ' for _ in range(10)] for _ in range(3)]
	for i, (_, r, c) in enumerate(coords):
		if i < len(letters_sorted):
			layout[r][c] = letters_sorted[i]

	return Layout(layout)

def make_random(base_layout: Layout) -> Layout:
	layout = base_layout.clone()

	positions = [(i, j) for i in range(len(layout.letters)) for j in range(len(layout.letters[0])) if layout.letters[i][j] != ' ']
	keys = [layout.letters[i][j] for i, j in positions]
	random.shuffle(keys)

	for idx, (i, j) in enumerate(positions):
		layout.letters[i][j] = keys[idx]

	return layout

def flatten(letters):
	return [item for row in letters for item in row]

def crossover(parents: list[Layout], blank=' '):
	def unflatten(flat, rows=ROWS, cols=COLS):
		return [flat[i*cols:(i+1)*cols] for i in range(rows)]

	parent1 = flatten(parents[0].letters)
	parent2 = flatten(parents[1].letters)
	length = len(parent1)

	a, b = sorted(random.sample(range(length), 2))
	child = [None] * length
	child[a:b] = parent1[a:b]

	for i in range(a, b):
		if parent2[i] not in parent1[a:b]:
			c = parent2[i]
			t = parent1[i]
			while t in parent2[a:b]:
				t = parent1[parent2.index(t)]
			if c not in child:
				j = parent2.index(t)
				if child[j] is None:
					child[j] = c

	for i in range(length):
		if child[i] is None:
			child[i] = parent2[i]

	return Layout(unflatten(child), source=parents[0].source+"->crossover")

def fine_tune_effort(base_layout: Layout):
	letters = [row[:] for row in base_layout.letters]
	positions = [(r,c) for r in range(3) for c in range(10) if letters[r][c] != ' ']
	positions.sort(key=lambda pos: LETTERS.get(letters[pos[0]][pos[1]],0), reverse=True)
	candidates = [base_layout.clone()]

	for (r,c) in positions:
		l = [row[:] for row in base_layout.letters]
		best = (r,c)
		for dr in (-1,0,1):
			for dc in (-1,0,1):
				nr,nc=r+dr,c+dc
				if 0<=nr<3 and 0<=nc<10 and l[nr][nc]!=' ':
					if EFFORT_GRID[nr][nc] < EFFORT_GRID[best[0]][best[1]]:
						best = (nr,nc)
		l[r][c], l[best[0]][best[1]] = l[best[0]][best[1]], l[r][c]
		candidates.append(Layout(l))

	best = best_layout(candidates)
	best.source = base_layout.source+"->fine_tune" if best != base_layout else base_layout.source
	return best

def optimize_effort(base_layout: Layout, result_len):
	orders = ['effort_asc', 'effort_desc', 'count_asc', 'count_desc']
	letters = [row[:] for row in base_layout.letters]
	layouts = {base_layout.clone()}

	for order in orders:
		effort_levels = list({val for row in EFFORT_GRID for val in row if val < 10})

		if order == 'effort_asc':
			effort_levels.sort()
		elif order == 'effort_desc':
			effort_levels.sort(reverse=True)
		else:
			effort_counts = {val: sum(1 for r in range(3) for c in range(10) if EFFORT_GRID[r][c] == val) for val in effort_levels}
			if order == 'count_asc':
				effort_levels.sort(key=lambda x: effort_counts[x])
			elif order == 'count_desc':
				effort_levels.sort(key=lambda x: -effort_counts[x])

		for effort_level in effort_levels:
			group_coords = [(r, c) for r in range(3) for c in range(10) if abs(EFFORT_GRID[r][c] - effort_level) <= 0.1]
			random.shuffle(group_coords)

			for i in range(len(group_coords)):
				r1, c1 = group_coords[i]
				for j in range(i+1, len(group_coords)):
					r2, c2 = group_coords[j]
					if letters[r1][c1] == ' ' and letters[r2][c2] == ' ':
						continue
					l = [row[:] for row in letters]
					l[r1][c1], l[r2][c2] = l[r2][c2], l[r1][c1]
					layouts.add(Layout(l, source=base_layout.source+"->effort"))

	return sort_unique_layouts(list(layouts), result_len)

def optimize_swap(base_layout: Layout, temperature, max_temp, fix=0):
	n = None
	t = temperature / max_temp
	if fix == 0:
		if t > 0.6:
			n = random.choices([6, 7, 8], weights=[0.4, 0.4, 0.2], k=1)[0]
		elif t > 0.2:
			n = random.choices([4, 5, 6], weights=[0.5, 0.3, 0.2], k=1)[0]
		else:
			n = random.choices([2, 3, 4], weights=[0.7, 0.2, 0.1], k=1)[0]
	else:
		n = fix

	coords = set()
	while len(coords) < n:
		r, c = random.randint(0, 2), random.randint(0, 9)
		if base_layout.letters[r][c] != ' ':
			coords.add((r, c))
	coords = list(coords)

	letters = [row[:] for row in base_layout.letters]

	shuffled = coords[:]
	random.shuffle(shuffled)

	for i in range(n):
		r1, c1 = coords[i]
		r2, c2 = shuffled[i]
		letters[r1][c1], letters[r2][c2] = letters[r2][c2], letters[r1][c1]

	return Layout(letters, source=base_layout.source)

def optimize_shuffle(base_layout: Layout, result_len, length=6, custom=""):
	if custom:
		letters = [l for l in custom]
	else:
		letters = random.sample(list(LETTERS.keys()), length)
	layouts = [base_layout.clone()]
	l = [row[:] for row in base_layout.letters]
	positions = [(r, c) for r in range(3) for c in range(10) if base_layout.letters[r][c] in letters]
	perms = permutations(letters, len(letters))

	for perm in perms:
		for (r, c), ch in zip(positions, perm):
			l[r][c] = ch
		layouts.append(Layout(l, source=base_layout.source+"->shuffle"))

	if custom:
		return sort_layouts(list(set(layouts)))[:result_len]
	else:
		return sort_unique_layouts(layouts, result_len)

def optimize_sa(base_layout: Layout, result_len, max_iter=10000, cooling_rate=0.9985, max_unimproved=2000):
	best = base_layout.clone()
	cur = base_layout.clone()
	initial_temp = max(abs(base_layout.total) * 0.005, 50)
	stop_temp = initial_temp * 1e-5
	temperature = initial_temp
	unimproved = 0
	result = [best.clone()]

	for i in range(max_iter):
		new_layout = optimize_swap(cur, temperature, initial_temp)
		diff = new_layout.total - cur.total

		if diff >= 0:
			accept = True
		else:
			T = max(temperature, 1e-9)
			prob = math.exp(diff / T)
			accept = prob > random.random()

		if accept:
			cur = new_layout
			if cur.total > best.total:
				best = cur.clone()
				best.source += f"->sa_{i}"
				result.append(best.clone())
				temperature *= 1.05
				unimproved = 0
		unimproved += 1
		temperature *= cooling_rate

		if unimproved > max_unimproved or temperature < stop_temp:
			break

	return sort_unique_layouts(result, result_len)

def optimize(base_layouts: list[Layout], result_path, elites_len=10):
	is_improved = False
	max_generation = elites_len*10
	max_population = elites_len*10
	elites = [l.clone() for l in base_layouts[:elites_len]]

	# Init population
	unique_population = {l.clone() for l in base_layouts}
	while len(unique_population) < max_population:
		unique_population.add(make_random(base_layouts[0]))
	population = sort_layouts(list(unique_population))
	
	with ProcessPoolExecutor() as executor:
		prev = elites[-1].total
		for gen in range(1, max_generation+1):
			print(f'\r\033[K...{gen}/{max_generation}', end='')
			random_len = int(max_population* max(0.05, 0.3 * (1 - gen/ max_generation)))
			elite_inject = max(1, round(elites_len * min(gen / (max_generation * 0.8), 1.0)))

			parents_pool = population + elites
			parents = [best_layout(random.sample(parents_pool, 3)) for _ in range(max_population)]
			children = [crossover(random.sample(parents, 2)) for _ in range(max_population - elite_inject - random_len)]

			# Make next
			population = []
			progress = min(gen/max_generation, 1.0)
			result = list(executor.map(
				optimize_worker,
				children + elites[:elite_inject],
				[progress] * (len(children)+elite_inject),
				[elites_len] * (len(children)+elite_inject)
			))
			for r in result:
				population.extend(r)
			population = sort_unique_layouts(population, max_population-random_len)
			while len(population) < max_population:
				population.append(make_random(elites[0]))
			population = sort_layouts(population)

			# Elites
			elites.extend([fine_tune_effort(l) for l in population])
			elites = sort_unique_layouts(elites, elites_len)

			if prev != elites[-1].total:
				is_improved = True
				print(f'\t improved', end='')

				enhanced_elites = [optimize_detail(e, elites_len) for e in elites]
				for e in enhanced_elites:
					elites.extend(e)
				elites = sort_unique_layouts(elites, elites_len)

				print(f' ({prev:,} -> {elites[-1].total:,})')
				print_layout(elites[0])
				print('')
				prev = elites[-1].total
				save_result(elites, result_path)

	enhanced_elites = [optimize_detail(e, elites_len) for e in elites]
	for e in enhanced_elites:
		elites.extend(e)
	elites = sort_unique_layouts(elites, elites_len)
	save_result(elites, result_path)
	return elites, is_improved

def optimize_worker(layout: Layout, progress, result_len):
	sa_weight = 0.2 + 0.2 * progress   # 0.2 - 0.4
	effort_weight = 0.2 + 0.1 * progress  # 0.2 - 0.3
	swap_weight = 0.3 - 0.05 * progress  # 0.3 - 0.25
	pass_weight = 1.0 - (sa_weight + effort_weight + swap_weight)

	weights = [max(0.0, sa_weight), max(0.0, effort_weight), max(0.0, swap_weight), max(0.0, pass_weight)]
	total = sum(weights)
	if total <= 0:
		weights = [0.25] * 4
		total = 1.0
	thresholds = []
	acc = 0.0
	for w in weights:
		acc += w / total
		thresholds.append(acc)

	r = random.random()
	if r < thresholds[0]:
		return optimize_sa(layout, result_len)
	elif r < thresholds[1]:
		return optimize_effort(layout, result_len)
	elif r < thresholds[2]:
		return optimize_shuffle(layout, result_len)
	else:
		return [layout]

def optimize_detail(layout: Layout, result_len, length=8):
	with ProcessPoolExecutor() as executor:
		result = []
		r = list(executor.map(
			optimize_shuffle,
			[layout] * multiprocessing.cpu_count(),
			[result_len] * multiprocessing.cpu_count(),
			[length] * multiprocessing.cpu_count()
		))
		for rr in r:
			result.extend(rr)

		return sort_unique_layouts(result, result_len)

def print_layout(layout: Layout):
	print(f'{layout.score.effort:,.0f}\t', end='')
	print(f'{layout.score.sfb:,.0f}\t', end='')
	print(f'{layout.score.rolling:,.0f}\t', end='')
	print(f'{layout.score.scissors:,.0f}')
	if layout.left_usage > 0:
		total = layout.left_usage + layout.right_usage
		left_percent = (layout.left_usage / total) * 100
		right_percent = (layout.right_usage / total) * 100
		print(f'{left_percent:.2f} : {right_percent:.2f} \t {layout.total:,}')
		print(f'{layout.source}')
	for row in layout.letters:
		print(row)

def save_result(layouts, result_path):
	file_path = os.path.join(result_path, RESULT_FILENAME)
	with open(file_path, 'w', encoding='utf-8') as f:
		for l in layouts:
			print(l.source, file=f)
			for row in l.letters:
				print(row, file=f)

def load_result(result_path):
	layouts = []
	file_path = os.path.join(result_path, RESULT_FILENAME)
	with open(file_path, 'r', encoding='utf-8') as f:
		lines = [line.strip() for line in f if line.strip()]
	for i in range(0, len(lines), 4):
		layouts.append(Layout([literal_eval(l) for l in lines[i+1:i+4]], source=lines[i]))
	return layouts

if __name__ == '__main__':
	multiprocessing.set_start_method("fork")
	signal.signal(signal.SIGINT, cleanup)
	try:
		if len(sys.argv) < 2:
			print(f"Usage: {sys.argv[0]} <result_path> [custom_index] [custom_letters]")
			sys.exit(1)

		result_path = sys.argv[1]
		result_path = os.path.expanduser(result_path)
		result_path = os.path.abspath(result_path)
		os.makedirs(result_path, exist_ok=True)

		# Analyze
		file_path = os.path.join(result_path, ANALYZE_RESULT_FILENAME)
		if os.path.exists(file_path):
			load_analysis_result(result_path)
		else:
			analyze_target(result_path)

		init_score_state()
		file_path = os.path.join(result_path, RESULT_FILENAME)
		if os.path.exists(file_path):
			result = load_result(result_path)
		else:
			result = [make_initial_layout()]

		if len(sys.argv) >= 3:
			if len(sys.argv) == 3:
				index = 0
				letters = sys.argv[2]
			else:
				index = int(sys.argv[2])
				letters = sys.argv[3]
			if letters != '':
				result = optimize_shuffle(result[index], len(letters), len(letters), letters)
		else:
			# Optimize
			is_improved = True
			r = 1
			while is_improved:
				print(f'[Optimize {r}]')
				result, is_improved = optimize(result, result_path)
				r += 1
			print(f'\r\033[K...Done')

		for i, l in enumerate(result, 1):
			print(f'[{i}]')
			print_layout(l)

	except KeyboardInterrupt:
		cleanup(None, None)

	cleanup(None,None)
