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
noremap r k
noremap e l
noremap S ^
noremap T <C-d>
noremap R <C-u>
noremap E $
noremap f b
noremap F B
noremap i w
noremap I W
" Mode
noremap p i
noremap P I
noremap y a
noremap Y A
noremap o v
noremap O V
noremap m o
noremap x O
noremap M R
noremap X r
" Operation
noremap n c
noremap N C
noremap v p
noremap V P
noremap c y
noremap c y
" Etc
noremap h :noh<CR>
noremap H <Plug>(YCMHover)
noremap w :write<CR>
noremap z za
noremap Z zR
noremap k n
noremap K N
noremap j :join!<CR>
noremap J :.-1join!<CR>
noremap a "
noremap A :registers<CR>
noremap U <C-r>
noremap l :call CycleList('l', 'n')<CR>
noremap L :call CycleList('l', 'p')<CR>
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
call Mapmap('<Leader>t', ':bprevious<CR>')
call Mapmap('<Leader>e', ':bnext<CR>')
" Sizing
call Mapmap('<Leader>+', '<C-w>5+')
call Mapmap('<Leader>-', '<C-w>5-')
call Mapmap('<Leader><', '<C-w>5<')
call Mapmap('<Leader>>', '<C-w>5>')
call Mapmap('<Leader>=', '<C-w>=')
call Mapmap('<Leader>_', '<C-w>_')
call Mapmap('<Leader>\|', '<C-w>\|')
" List
call Mapmap('<Leader>m', ':call ToggleList("l")<CR>')
call Mapmap('<Leader>x', ':call ToggleList("c")<CR>')
call Mapmap('<Leader>l', ':call CycleList("c","n")<CR>')
call Mapmap('<Leader>L', ':call CycleList("c","p")<CR>')
" YCM
call Mapmap('<Leader>p', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>r', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>g', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>f', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader>s', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='r'
let g:NERDTreeMenuDown='t'
let g:NERDTreeMapRefresh='s'
let g:NERDTreeMapCustomOpen='e'
" Tagbar
call Mapmap('<Leader>j', ':TagbarToggle<CR>')
let g:tagbar_map_togglecaseinsensitive = ""
let g:tagbar_map_togglesort = ""
let g:tagbar_map_togglepause = ""
let g:tagbar_map_jump = "s"
" Etc
call Mapmap('<Leader>b', '<C-o>')
call Mapmap('<Leader>B', '<C-i>')
