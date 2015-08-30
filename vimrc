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
augroup Hieratime
  autocmd!
  autocmd BufRead,BufNewFile *.hieratime setlocal foldmethod=expr foldexpr=HieratimeFold() foldtext=HieratimeFoldText() fillchars=vert\:\|,fold:\  nonumber
  autocmd BufRead,BufNewFile *.hieratime highlight Folded NONE
  autocmd BufRead,BufNewFile *.hieratime nnoremap <buffer> <C-H><C-I> :py hieratime.clock_in()<CR>
  autocmd BufRead,BufNewFile *.hieratime nnoremap <buffer> <C-H><C-O> :py hieratime.clock_out()<CR>
  autocmd BufRead,BufNewFile *.hieratime nnoremap <buffer> <C-H><C-H> :py hieratime.refresh()<CR>
augroup end
