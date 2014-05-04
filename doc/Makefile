.PHONY: setup clean distclean 

setup: 
	@echo  -n "Initiate ..."
	@mkdir -p report tmp
	@echo "\t\t[DONE]"

report: setup src/report.tex
	@echo -n "Compiling ..."
	@cp -r src/* tmp
	@cd tmp ;\
	pdflatex -halt-on-error -interaction=nonstopmode report.tex make d  > texoutput.log ;\
	bibtex report  > biboutput.log ;\
	pdflatex -halt-on-error -interaction=nonstopmode report.tex make d  > texoutput.log ;\
	pdflatex -halt-on-error -interaction=nonstopmode report.tex make d  > texoutput.log ;\
	cp *.pdf ../report
	@echo "\t\t[DONE]"

clean:
	@rm -rf log tmp
	@echo -n "Cleaning ...."
	@echo "\t\t[DONE]"

distclean: clean
	@rm -rf report