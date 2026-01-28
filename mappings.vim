"
" Mapping
"
let mapleader=','
function! Mapmap(lhs, rhs)
  execute 'map '.a:lhs.' '.a:rhs
  execute 'imap '.a:lhs.' <Esc>'.a:rhs
endfunction
" Cursor
noremap c h
noremap t j
noremap r k
noremap e l
noremap C ^
noremap T <C-d>
noremap R <C-u>
noremap E $
" Mode
noremap d r
noremap D R
" Operation
noremap m c
noremap M C
noremap h d
noremap H D
" Etc
noremap q @
noremap Q q
noremap z za
noremap Z zR
noremap j :join!<CR>
noremap J :.-1join!<CR>
noremap k "
noremap K :registers<CR>
noremap U <C-r>
noremap l g;
noremap L g,
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
call Mapmap('<Leader>s', ':bprevious<CR>')
call Mapmap('<Leader>o', ':bnext<CR>')
" Sizing
call Mapmap('<Leader>+', '<C-w>5+')
call Mapmap('<Leader>-', '<C-w>5-')
call Mapmap('<Leader><', '<C-w>5<')
call Mapmap('<Leader>>', '<C-w>5>')
call Mapmap('<Leader>=', '<C-w>=')
call Mapmap('<Leader>_', '<C-w>_')
call Mapmap('<Leader>\|', '<C-w>\|')
" List
call Mapmap('<Leader>t', ':call ToggleList("l")<CR>')
call Mapmap('<Leader>r', ':call ToggleList("c")<CR>')
call Mapmap('<Leader>h', ':call CycleList("c","n")<CR>')
call Mapmap('<Leader>H', ':call CycleList("c","p")<CR>')
call Mapmap('<Leader>m', ':call CycleList("l","n")<CR>')
call Mapmap('<Leader>M', ':call CycleList("l","p")<CR>')
" YCM
call Mapmap('<Leader>p', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>G', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>g', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>f', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader>c', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='r'
let g:NERDTreeMenuDown='t'
let g:NERDTreeMapRefresh='c'
let g:NERDTreeMapCustomOpen='e'
" Tagbar
call Mapmap('<Leader>e', ':TagbarToggle<CR>')
let g:tagbar_map_togglecaseinsensitive = ""
let g:tagbar_map_togglesort = ""
let g:tagbar_map_togglepause = ""
let g:tagbar_map_jump = "c"
" Etc
call Mapmap('<Leader>l', '<C-o>')
call Mapmap('<Leader>L', '<C-i>')
call Mapmap('<Leader>j', ':noh<CR>')
call Mapmap('<Leader>J', '<Plug>(YCMHover)')
