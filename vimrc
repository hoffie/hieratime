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

pyf /path/to/hieratime.py
augroup Hieratime
  autocmd!
  autocmd BufRead *.hieratime setlocal foldmethod=expr foldexpr=HieratimeFold() foldtext=HieratimeFoldText() fillchars=vert\:\|,fold:\ 
  " The following highlighting change may possibly affect other buffers. To be
  " tested/fixed.
  autocmd BufRead *.hieratime highlight Folded guibg=bg guifg=fg
  autocmd BufRead *.hieratime nnoremap <buffer> <C-H><C-I> :py vim_clock_in()<CR>
  autocmd BufRead *.hieratime nnoremap <buffer> <C-H><C-O> :py vim_clock_out()<CR>
  autocmd BufRead *.hieratime nnoremap <buffer> <C-H><C-H> :py vim_refresh()<CR>
augroup end

