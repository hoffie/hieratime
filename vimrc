" Append this code to your .vimrc. Adapt as needed.

function! HieratimeFold()
  let h = matchstr(getline(v:lnum), '^\*\+')
  if empty(h)
    return "="
  else
    return ">" . len(h)
  endif
endfunction

function! HieratimeFoldText()
  return getline(v:foldstart) . "..."
endfunction

py sys.path.insert(0, '/path/to/hieratime/')
py from hieratime import vim_integration as hieratime
py reload(hieratime)
augroup Hieratime
  autocmd!
  autocmd BufRead *.hieratime setlocal foldmethod=expr foldexpr=HieratimeFold() foldtext=HieratimeFoldText() fillchars=vert\:\|,fold:\ 
  autocmd BufRead *.hieratime highlight Folded guibg=bg guifg=fg
  autocmd BufRead *.hieratime nnoremap <buffer> <C-H><C-I> :py hieratime.clock_in()<CR>
  autocmd BufRead *.hieratime nnoremap <buffer> <C-H><C-O> :py hieratime.clock_out()<CR>
  autocmd BufRead *.hieratime nnoremap <buffer> <C-H><C-H> :py hieratime.refresh()<CR>
augroup end
