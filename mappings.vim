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
noremap n l
noremap T ^
noremap I <C-d>
noremap E <C-u>
noremap N $
noremap c b
noremap C B
noremap r w
noremap R W
" Mode
noremap l o
noremap a O
noremap L r
noremap A R
noremap d i
noremap D I
noremap s a
noremap S A
" Operation
noremap h c
noremap H C
noremap o d
noremap O D
" Etc
noremap m @
noremap M q
noremap w :write<CR>
noremap z za
noremap Z zR
noremap k n
noremap K N
noremap j :join!<CR>
noremap J :.-1join!<CR>
noremap q "
noremap Q :registers<CR>
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
call Mapmap('<Leader>z', ':wqall<CR>')
call Mapmap('<Leader>X', '<C-w>c')
call Mapmap('<Leader>s', ':split<CR>')
call Mapmap('<Leader>S', ':vsplit<CR>')
" Buffer
call Mapmap('<Leader>x', ':call CloseBuf()<CR>')
call Mapmap('<Leader>i', ':bprevious<CR>')
call Mapmap('<Leader>n', ':bnext<CR>')
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
call Mapmap('<Leader>l', ':call CycleList("l","n")<CR>')
call Mapmap('<Leader>L', ':call CycleList("l","p")<CR>')
" YCM
call Mapmap('<Leader>p', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>G', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>g', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>f', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader>c', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='e'
let g:NERDTreeMenuDown='i'
let g:NERDTreeMapRefresh='t'
let g:NERDTreeMapCustomOpen='n'
" Tagbar
call Mapmap('<Leader>r', ':TagbarToggle<CR>')
let g:tagbar_map_togglecaseinsensitive = ""
let g:tagbar_map_togglesort = ""
let g:tagbar_map_togglepause = ""
let g:tagbar_map_jump = "t"
" Etc
call Mapmap('<Leader>b', '<C-o>')
call Mapmap('<Leader>B', '<C-i>')
call Mapmap('<Leader>m', ':noh<CR>')
call Mapmap('<Leader>M', '<Plug>(YCMHover)')
