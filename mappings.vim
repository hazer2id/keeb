"
" Mapping
"
let mapleader=','
function! Mapmap(lhs, rhs)
  execute 'map '.a:lhs.' '.a:rhs
  execute 'imap '.a:lhs.' <Esc>'.a:rhs
endfunction
" Cursor
noremap t h
noremap i j
noremap e k
noremap r l
noremap T ^
noremap I <C-d>
noremap E <C-u>
noremap R $
noremap d b
noremap D B
noremap n w
noremap N W
" Mode
noremap p o
noremap a O
noremap A r
noremap P R
noremap m i
noremap M I
noremap s a
noremap S A
noremap l v
noremap L V
noremap <C-l> <C-v>
" Operation
noremap h c
noremap H C
noremap o d
noremap O D
noremap c y
noremap C Y
noremap v p
noremap V P
" Etc
noremap q :write<CR>
noremap f za
noremap F zR
noremap k n
noremap K N
noremap j :join!<CR>
noremap J :.-1join!<CR>
noremap y "
noremap Y :registers<CR>
noremap U <C-r>
noremap b g;
noremap B g,
noremap <Space> o<Esc>
noremap <BackSpace> X
noremap ( [(
noremap ) ])
noremap { [{
noremap } ]}
noremap ; %
noremap + <C-a>
noremap - <C-x>

" Cursor
call Mapmap('<Leader><Left>',  '<C-w>h')
call Mapmap('<Leader><Right>', '<C-w>l')
call Mapmap('<Leader><Up>',    '<C-w>k')
call Mapmap('<Leader><Down>',  '<C-w>j')
call Mapmap('<PageUp>',        '<C-b>')
call Mapmap('<PageDown>',      '<C-f>')
" Window
call Mapmap('<Leader>q', ':wqall<CR>')
call Mapmap('<Leader>C', '<C-w>c')
call Mapmap('<Leader>Z', ':vsplit<CR>')
call Mapmap('<Leader>z', ':split<CR>')
" Buffer
call Mapmap('<Leader>c', ':call CloseBuf()<CR>')
call Mapmap('<Leader>i', ':bprevious<CR>')
call Mapmap('<Leader>r', ':bnext<CR>')
" Sizing
call Mapmap('<Leader>+', '<C-w>5+')
call Mapmap('<Leader>-', '<C-w>5-')
call Mapmap('<Leader><', '<C-w>5<')
call Mapmap('<Leader>>', '<C-w>5>')
call Mapmap('<Leader>=', '<C-w>=')
call Mapmap('<Leader>_', '<C-w>_')
call Mapmap('<Leader>\|', '<C-w>\|')
" List
call Mapmap('<Leader>h', ':call ToggleList("l")<CR>')
call Mapmap('<Leader>o', ':call ToggleList("c")<CR>')
call Mapmap('<Leader>a', ':call CycleList("c","n")<CR>')
call Mapmap('<Leader>A', ':call CycleList("c","p")<CR>')
call Mapmap('<Leader>p', ':call CycleList("l","n")<CR>')
call Mapmap('<Leader>P', ':call CycleList("l","p")<CR>')
" YCM
call Mapmap('<Leader>t', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>G', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>g', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>f', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader>d', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='e'
let g:NERDTreeMenuDown='i'
let g:NERDTreeMapRefresh='t'
let g:NERDTreeMapCustomOpen='r'
" Tagbar
call Mapmap('<Leader>n', ':TagbarToggle<CR>')
let g:tagbar_map_togglecaseinsensitive = ""
let g:tagbar_map_togglesort = ""
let g:tagbar_map_togglepause = ""
let g:tagbar_map_jump = "t"
" Etc
call Mapmap('<Leader>b', '<C-o>')
call Mapmap('<Leader>B', '<C-i>')
call Mapmap('<Leader>k', ':noh<CR>')
call Mapmap('<Leader>K', '<Plug>(YCMHover)')
