"
" Mapping
"
let mapleader=','
function! Mapmap(lhs, rhs)
  execute 'map '.a:lhs.' '.a:rhs
  execute 'imap '.a:lhs.' <Esc>'.a:rhs
endfunction
" Cursor
noremap r h
noremap e j
noremap n k
noremap t l
noremap R ^
noremap E <C-d>
noremap N <C-u>
noremap T $
noremap k b
noremap K B
noremap d w
noremap D W
" Mode
noremap l o
noremap L O
noremap s r
noremap S R
" Operation
noremap o c
noremap O C
noremap c d
noremap C D
" Etc
noremap w :write<CR>
noremap f za
noremap F zR
noremap h n
noremap H N
noremap j :join!<CR>
noremap J :.-1join!<CR>
noremap m "
noremap M :registers<CR>
noremap U <C-r>
noremap b g;
noremap B g,
noremap q @
noremap Q q
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
call Mapmap('<Leader>Z', ':vsplit<CR>')
call Mapmap('<Leader>z', ':split<CR>')
" Buffer
call Mapmap('<Leader>x', ':call CloseBuf()<CR>')
call Mapmap('<Leader>e', ':bprevious<CR>')
call Mapmap('<Leader>t', ':bnext<CR>')
" Sizing
call Mapmap('<Leader>+', '<C-w>5+')
call Mapmap('<Leader>-', '<C-w>5-')
call Mapmap('<Leader><', '<C-w>5<')
call Mapmap('<Leader>>', '<C-w>5>')
call Mapmap('<Leader>=', '<C-w>=')
call Mapmap('<Leader>_', '<C-w>_')
call Mapmap('<Leader>\|', '<C-w>\|')
" List
call Mapmap('<Leader>o', ':call ToggleList("l")<CR>')
call Mapmap('<Leader>c', ':call ToggleList("c")<CR>')
call Mapmap('<Leader>s', ':call CycleList("c","n")<CR>')
call Mapmap('<Leader>S', ':call CycleList("c","p")<CR>')
call Mapmap('<Leader>a', ':call CycleList("l","n")<CR>')
call Mapmap('<Leader>A', ':call CycleList("l","p")<CR>')
" YCM
call Mapmap('<Leader>p', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>r', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>g', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>f', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader>k', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='r'
let g:NERDTreeMenuDown='e'
let g:NERDTreeMapRefresh='n'
let g:NERDTreeMapCustomOpen='t'
" Tagbar
call Mapmap('<Leader>d', ':TagbarToggle<CR>')
let g:tagbar_map_togglecaseinsensitive = ""
let g:tagbar_map_togglesort = ""
let g:tagbar_map_togglepause = ""
let g:tagbar_map_jump = "r"
" Etc
call Mapmap('<Leader>b', '<C-o>')
call Mapmap('<Leader>B', '<C-i>')
call Mapmap('<Leader>h', ':noh<CR>')
call Mapmap('<Leader>H', '<Plug>(YCMHover)')
