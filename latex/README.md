# Basic instructions
Always save all the files in UTF8 format.

## Template
The `report_requirements.tex` file uses a custom made template: `sgreport.cls`.

To get correct references and page numbers in the output pdf compile the `report_requirements.tex` file twice.

## Add a chapter
Create a new file `chapter_X.tex` under `chapters/` and include it in the main `report_requirements.tex` file with the command `\include{chapter_X}`

## Glossary
The glossary file `glossarry.tex` is located under `glossary/`

There are two types of glossary entries: acronyms and glossary entries.

To create a new glossary entry insert in `glossarry.tex` either:

* An acronym:

```latex
\newacronym{⟨label⟩}{⟨short⟩}{⟨long⟩}
```

* A glossary entry:

```latex
\newglossaryentry{⟨label⟩} 
{ 
  name={⟨name⟩}, 
  description={⟨description⟩}, 
  ⟨other options⟩ 
}
```

Then build the `report_requirements`, build glossary using makeglossary (`makeglossary report_requirements`), build `report_requirements` again.

See the [Wikibook section about glossaries][WGL] to see how to use a term in the document. 

[Short guide for glossaries][GLG]
[CTAN Reference][CTAN-GL]

## Bibliography
* The `.bib` file is located under `bibliography/p1_bib.bib`

Example: 

```latex
@book{ab94,
   author* = {Charalambos D. Aliprantis and Kim C. Border},
   year = {1994},
   title = {Infinite Dimensional Analysis},
   publisher = {Springer},
   address = {Berlin}
}
```
To cite the book just insert `\cite{ab94}` in the document

Then build the bibliography:

```shell
$ latex report_requirements
$ biber report_requirements
$ latex report_requirements
$ latex report_requirements
```
Usually there is a macro in your favourite LaTeX editor to build bibliographies. Make sure that you use biber and not bibtex. Look here on how to [configure your editor][COE]
 
[Short guide about BibTeX][SGB]
To add a reference use a program from [Programs](#programs)

## Latexmk
**To compile everything automatically and the good number of times use [latexmk][LATEXMK].**

Use the following configuration file:

```bash
$pdf_mode = 1;
$bibtex_use = 2;
$pdflatex = 'pdflatex --shell-escape %O %S';
$pdf_previewer = 'open -a Preview "%S"';

add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');

sub run_makeglossaries {
    my ($base_name, $path) = fileparse( $_[0] );
    pushd $path;
    
    if ( $silent ) {
        system "makeglossaries -q '$base_name'";
    }
    else {
        system "makeglossaries '$base_name'";
    };
    popd;
}

push @generated_exts, 'glo', 'gls', 'glg';
push @generated_exts, 'acn', 'acr', 'alg';
$clean_ext .= ' %R.ist %R.xdy';
$out_dir = 'build';
```
You should edit the line 4 and specify your own pdf viewer. The example above is configured for macOS.

## LaTeX syntax
* Avoid spaces after `\item`

```latex
...
	\item\label{...}
...
```

* If there is a space before a command use a tilde after the command and not a space.

```latex
... some text \textgreater~some other text ...
```

* If there is a carriage return after a command without option (`\latexcommand`) put empty braces after it (`\latexcommand{}`) to avoid warnings.

* For DVI output: Always specify the image size in pixel when you include one

```latex
\begin{figure}
    \centering
    \includegraphics[width=0.8\textwidth,natwidth=610,natheight=642]{tiger.pdf}
\end{figure}
```

* **Label names should be unique!**


## Programs
* [Zotero][ZTO]: Save books, links, video references quickly. Need to setup Default Output Format (Preferences->Export). Allows drag&drop to tools like Bibdesk and Jabref.
* [Jabref][JBF]: Like [Bibdesk][BD], manage .bib files but cross platform compatible.
* [Other Alternatives][OT]

[BD]:http://bibdesk.sourceforge.net
[CTAN-GL]:http://ctan.sharelatex.com/tex-archive/macros/latex/contrib/glossaries/glossariesbegin.html#sec:defterm
[COE]:http://tex.stackexchange.com/questions/154751/biblatex-with-biber-configuring-my-editor-to-avoid-undefined-citations
[GLG]:https://philmikejones.wordpress.com/2015/02/27/glossary-acronyms-latex/
[JBF]:http://www.jabref.org
[OT]:http://mactex-wiki.tug.org/wiki/index.php?title=GUI_Tools#Bibliographies
[SGB]:https://www.economics.utoronto.ca/osborne/latex/BIBTEX.HTM
[WGL]:https://en.wikibooks.org/wiki/LaTeX/Glossary#Using_defined_terms
[ZTO]:https://www.zotero.org
[LATEXMK]:http://mg.readthedocs.io/latexmk.html