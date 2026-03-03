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
noremap s j
noremap e k
noremap r l
noremap T ^
noremap S <C-d>
noremap E <C-u>
noremap R $
noremap w e
noremap W w
" Mode
noremap l s
noremap L R
" Operation
" Etc
noremap k :call CycleList("l","n")<CR>
noremap K :call CycleList("l","p")<CR>
noremap h noh<CR>
noremap H <Plug>(YCMHover)
noremap q @
noremap Q q
noremap x za
noremap Z zR
noremap z :join!<CR>
noremap Z :.-1join!<CR>
noremap m "
noremap M :registers<CR>
noremap U <C-r>
noremap j g;
noremap J g,
noremap <Space> o<Esc>
noremap <Backspace> X
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
call Mapmap('<Leader>z', ':split<CR>')
call Mapmap('<Leader>Z', ':vsplit<CR>')
" Buffer
call Mapmap('<Leader>x', ':call CloseBuf()<CR>')
call Mapmap('<Leader>n', ':bprevious<CR>')
call Mapmap('<Leader>c', ':bnext<CR>')
" Sizing
call Mapmap('<Leader>+', '<C-w>5+')
call Mapmap('<Leader>-', '<C-w>5-')
call Mapmap('<Leader><', '<C-w>5<')
call Mapmap('<Leader>>', '<C-w>5>')
call Mapmap('<Leader>=', '<C-w>=')
call Mapmap('<Leader>_', '<C-w>_')
call Mapmap('<Leader>\|', '<C-w>\|')
" List
call Mapmap('<Leader>s', ':call ToggleList("l")<CR>')
call Mapmap('<Leader>e', ':call ToggleList("c")<CR>')
call Mapmap('<Leader>k', ':call CycleList("c","n")<CR>')
call Mapmap('<Leader>K', ':call CycleList("c","p")<CR>')
" YCM
call Mapmap('<Leader>a', ':YcmCompleter GoToAlternateFile<CR>')
call Mapmap('<Leader>G', ':YcmCompleter GoToReferences<CR>:call AfterYcm()<CR>')
call Mapmap('<Leader>g', ':YcmCompleter GoTo<CR>')
call Mapmap('<Leader>f', '<Plug>(YCMFindSymbolInWorkspace)')
" Nerdtree
call Mapmap('<Leader>t', ':NERDTreeToggle<CR>')
let g:NERDTreeMenuUp='s'
let g:NERDTreeMenuDown='e'
let g:NERDTreeMapRefresh='t'
let g:NERDTreeMapCustomOpen='r'
" Tagbar
call Mapmap('<Leader>r', ':TagbarToggle<CR>')
let g:tagbar_map_togglecaseinsensitive = ""
let g:tagbar_map_togglesort = ""
let g:tagbar_map_togglepause = ""
let g:tagbar_map_jump = "t"
" Etc
call Mapmap('<Leader>j', '<C-o>')
call Mapmap('<Leader>J', '<C-i>')
