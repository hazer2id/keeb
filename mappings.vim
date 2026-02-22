"
" Mapping
"
let mapleader=','
function! Mapmap(lhs, rhs)
  execute 'map '.a:lhs.' '.a:rhs
  execute 'imap '.a:lhs.' <Esc>'.a:rhs
endfunction
" Cursor
noremap <Space> h
noremap r j
noremap e k
noremap t l
noremap d b
noremap D B
noremap s w
noremap S W
" Mode
noremap l o
noremap L O
noremap a i
noremap A a
noremap c s
noremap C R
" Operation
noremap i d
noremap I D
noremap n c
noremap N C
" Etc
noremap m @
noremap M q
noremap w :write<CR>
noremap f za
noremap F zR
noremap k n
noremap K N
noremap j :join!<CR>
noremap J :.-1join!<CR>
noremap o "
noremap O :registers<CR>
noremap U <C-r>
noremap b g;
noremap B g,
noremap w :write<CR>
noremap m :noh<CR>
noremap M <Plug>(YCMHover)
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
call Mapmap('<Leader>s', ':split<CR>')
call Mapmap('<Leader>S', ':vsplit<CR>')
" Buffer
call Mapmap('<Leader>c', ':call CloseBuf()<CR>')
call Mapmap('<Leader>_', ':bprevious<CR>')
call Mapmap('<Leader>.', ':bnext<CR>')
" Sizing
call Mapmap('<Leader>+', '<C-w>5+')
call Mapmap('<Leader>-', '<C-w>5-')
call Mapmap('<Leader><', '<C-w>5<')
call Mapmap('<Leader>>', '<C-w>5>')
call Mapmap('<Leader>=', '<C-w>=')
call Mapmap('<Leader>_', '<C-w>_')
call Mapmap('<Leader>\|', '<C-w>\|')
" List
call Mapmap('<Leader>r', ':call ToggleList("l")<CR>')
call Mapmap('<Leader>e', ':call ToggleList("c")<CR>')
call Mapmap('<Leader>i', ':call CycleList("c","n")<CR>')
call Mapmap('<Leader>I', ':call CycleList("c","p")<CR>')
call Mapmap('<Leader>n', ':call CycleList("l","n")<CR>')
call Mapmap('<Leader>N', ':call CycleList("l","p")<CR>')
" YCM
call Mapmap('<Leader>p', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>G', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>g', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>f', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader><Space>', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='e'
let g:NERDTreeMenuDown='r'
let g:NERDTreeMapRefresh='<Space>'
let g:NERDTreeMapCustomOpen='t'
" Tagbar
call Mapmap('<Leader>t', ':TagbarToggle<CR>')
let g:tagbar_map_showproto=''
let g:tagbar_map_togglepause = ''
let g:tagbar_map_jump = '<Space>'
" Etc
call Mapmap('<Leader>b', '<C-o>')
call Mapmap('<Leader>B', '<C-i>')
