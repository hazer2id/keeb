"
" Mapping
"
let mapleader=','
function! Mapmap(lhs, rhs)
  execute 'map '.a:lhs.' '.a:rhs
  execute 'imap '.a:lhs.' <Esc>'.a:rhs
endfunction
" Cursor
noremap s h
noremap t j
noremap e k
noremap r l
noremap S ^
noremap T <C-d>
noremap E <C-u>
noremap R $
noremap x b
noremap X B
noremap n w
noremap N W
" Mode
noremap y i
noremap Y I
noremap l a
noremap L A
noremap o v
noremap O V
noremap p o
noremap a O
" Operation
noremap f c
noremap F C
noremap i d
noremap I D
noremap c y
noremap c y
" Etc
noremap v p
noremap V P
noremap z :write<CR>
noremap w r
noremap W R
noremap q za
noremap Q zR
noremap h n
noremap H N
noremap j :join!<CR>
noremap J :.-1join!<CR>
noremap k "
noremap K :registers<CR>
noremap U <C-r>
noremap m :call CycleList('l', 'n')<CR>
noremap M :call CycleList('l', 'p')<CR>
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
call Mapmap('<Leader>X', '<C-w>c')
call Mapmap('<Leader>h', ':vsplit<CR>')
call Mapmap('<Leader>v', ':split<CR>')
" Buffer
call Mapmap('<Leader>x', ':call CloseBuf()<CR>')
call Mapmap('<Leader>t', ':bprevious<CR>')
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
call Mapmap('<Leader>f', ':call ToggleList("l")<CR>')
call Mapmap('<Leader>i', ':call ToggleList("c")<CR>')
call Mapmap('<Leader>m', ':call CycleList("c","n")<CR>')
call Mapmap('<Leader>M', ':call CycleList("c","p")<CR>')
" YCM
call Mapmap('<Leader>y', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>a', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>p', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>e', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader>s', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='e'
let g:NERDTreeMenuDown='t'
let g:NERDTreeMapRefresh='s'
let g:NERDTreeMapCustomOpen='r'
" Tagbar
call Mapmap('<Leader>n', ':TagbarToggle<CR>')
let g:tagbar_map_togglecaseinsensitive = ""
let g:tagbar_map_togglesort = ""
let g:tagbar_map_togglepause = ""
let g:tagbar_map_jump = "s"
" Etc
call Mapmap('<Leader>b', '<C-o>')
call Mapmap('<Leader>B', '<C-i>')
call Mapmap('<Leader>l', ':noh<CR>')
call Mapmap('<Leader>L', '<Plug>(YCMHover)')
