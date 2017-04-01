\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{thesis}[2016/03/30 A thesis template licensed to Department of Information Technology in Tallinn University of Technology]

% Load basic documentclass book
%
\LoadClass[12pt]{article}

% Paper size and margins

%\RequirePackage[a4paper, top=2.5cm, bottom=2.5cm, left=3cm, right=3cm, showframe]{geometry}
%\RequirePackage[a4paper]{geometry} %Lisades käsu ", showframe" saab näha lehe servi

\RequirePackage{layout}
% Loading required packages

\RequirePackage{tikz-timing}
\RequirePackage{tikz}
\RequirePackage{circuitikz}
\usetikzlibrary{arrows,shapes}
\usetikzlibrary{decorations.pathreplacing}
\RequirePackage{fancybox}
\RequirePackage{nicefrac} %Vajalik ilusate murdude tegemiseks
\RequirePackage{amsmath} %Võimaldab joondada valemeid vasakusse serva
\RequirePackage{subcaption} %Kasutusel kui mitu pilti on ühel real
\RequirePackage{listings} %Programmi koodid
\RequirePackage{titlesec} %Vajalik pealkirjade modifitseerimiseks
\RequirePackage[hang,flushmargin,perpage]{footmisc} %Eemaldab allmärkuste juurest eraldava joone
\RequirePackage[hidelinks]{hyperref} %Links and navigation
\RequirePackage{hypcap} %Links anchor to images not captions

\titleformat{\section}[block] %I taseme nummerdatud pealkirjade suurus ja formaat
{\newpage\fontsize{16}{10}\bfseries\vspace*{0pt}}
{\thesection}
{5pt}
{}

\titlespacing{\section}{0pt}{60pt}{18pt} %I taseme nummerdatud pealkirjade vahed

\titleformat{\subsection}[block] %II taseme pealkirjade suurus ja formaat
{\fontsize{14}{15}\bfseries\vspace{10pt}}
{\thesubsection}
{5pt}
{}

\titlespacing{\subsection}{0pt}{0pt}{0pt} %II taseme pealkirjade vahed

\titleformat{\subsubsection}[block] %III taseme pealkirjade suurus ja formaat
{\fontsize{12}{15}\bfseries\vspace{12pt}}
{\thesubsubsection}
{5pt}
{}

\titlespacing{\subsubsection}{0pt}{0pt}{0pt} %III taseme pealkirjade vahed

%\setcounter{secnumdepth}{3}

%\setlength{\mathindent}{0cm}

\headheight = 0pt %Paneb paika päise laiuse
\headsep = 0pt %Vähendab päise ja teksti vahelise kauguse nullini
\setlength{\topmargin}{0pt} 
%\setlength{\footskip}{1cm}
\setlength{\oddsidemargin}{0pt}
\setlength{\marginparsep}{0pt}
\setlength{\marginparwidth}{0pt}
\setlength{\textheight}{701pt}
\setlength{\textwidth}{427pt}
%\renewcommand{\footrulewidth}{20pt}
%\footskip = 20pt
\setlength{\voffset}{-0.2in}


\RequirePackage{listings} %Vajalik koodi formaatimiseks tekstis
\lstdefinestyle{customc}{ %C programmi kujunduslik vormindamine
	belowcaptionskip=1\baselineskip,
	breaklines=true,
	xleftmargin=\parindent,
	language=C,
	showstringspaces=false,
	basicstyle=\footnotesize\ttfamily,
	keywordstyle=\bfseries\color{green!40!black},
	commentstyle=\itshape\color{purple!40!black},
	identifierstyle=\color{blue},
	stringstyle=\color{orange},
}
%Lisanäiteid programmikoodi formaatimisest leiab siit: https://en.wikibooks.org/wiki/LaTeX/Source_Code_Listings#Supported_languages


\RequirePackage{longtable} %Vajalik pakett, et saaks teha üle ühe leheküljelisi tabeleid
\RequirePackage{multirow} %Vajalik, kui tahta tabelites mitut rida kokku panna
\RequirePackage{todonotes} %Vajalik, kui tahta lisada töösse todo märkmeid
\RequirePackage{url} %Vajalik, kui töös on kasutusel URL aadress. Sel juhul märkida URL tagi vahele ning LaTeX ei hakka seda lahti kompileerima eraldi käskudeks vms
\RequirePackage{float} %Vajalik töös olevate tabelite ja jooniste vormistamiseks

\RequirePackage[english]{babel} %Vene ja eesti keelsete tähtede kasutamise võimalus
%	\addto\captionsestonian{\def\refname{{Kasutatud kirjandus}}} %Muudab viidete nime kasutatud kirjanduseks ning paigutab lehe keskele
%	\addto\captionsestonian{\def\listfigurename{\centerline{Jooniste loetelu}}} %Muudab jooniste nimekirja nime jooniste loeteluks ning paigutab selle lehe keskele
%	\addto\captionsestonian{\def\listtablename{\centerline{Tabelite loetelu}}} %Muudab tabelite nimekirja nime tabelite loeteluks ning paigutab selle lehe keskele
%	\addto\captionsestonian{\def\contentsname{\centerline{Sisukord}}}
\RequirePackage[T1]{fontenc} %Vajalik eesti  keelsete tähtede kasutamiseks
%\RequirePackage[utf8]{inputenc} %UTF8 dekodeerimist kasutatakse

\RequirePackage{tocloft} %Selleks, et modida sisukordi!

%\renewcommand{\cftfigpresnum}{\figurename\enspace}
%\renewcommand{\cftfigaftersnum}{:}
%\settowidth{\enskip}{\cftfigpresnum\cftfigaftersnum}
%\addtolength{\cftfignumwidth}{\enskip}

%\renewcommand*\cftfigpresnum{Joonis~} %Selleks, et lisada sõna Joonis jooniste loetelusse
%\settowidth{\cftfignumwidth}{\cftfigpresnum} %Lisab numbri pärast sõna Joonis
%\renewcommand{\cftfigaftersnumb}{ .\enskip} %Lisab punkti ning tühiku pärast Joonise numbrit

%\renewcommand*\cfttabpresnum{Tabel~} %Selleks, et lisada sõna Joonis jooniste loetelusse
%\settowidth{\cfttabnumwidth}{\cfttabpresnum} %Lisab numbri pärast sõna Joonis
%\renewcommand{\cfttabaftersnumb}{ .\enskip} %Lisab punkti ning tühiku pärast Joonise numbrit


\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}} %Selleks, et sisukorras oleks "sectioni" järel punktid
\renewcommand\cftsecfont{\mdseries} %Sisukorra pealkirjad mitte "bold"
\renewcommand\cftsecpagefont{\mdseries} %Sisukorra lehenumbrid mitte "bold"
\setlength\cftsubsecindent{0,42cm} %Sisukorras erinevate pealkirjade taanded
\setlength\cftsubsubsecindent{0,85cm} %Sisukorras erinevate pealkirjade taanded
\setlength\cftbeforesecskip{0cm} %Sisukorras erinevate pealkirjade taanded

\RequirePackage{gensymb}
\RequirePackage{amssymb} %For square itemized listss
\renewcommand{\labelitemi}{\tiny$\blacksquare$} %For square itemized lists


\RequirePackage[font=footnotesize]{caption} %Vajalik tabelite ja jooniste pealkirjastamisel
\captionsetup{labelsep=period} %Lisab tabeli või joonise nime lõppu punkti

\RequirePackage{verbatimbox} %To put program code in the center using Verbatim

\titlelabel{\thetitle.\quad} %Lisab pealkirjade lõppu punkti
%\titlespacing\section{100pt}{12pt plus 4pt minus 2pt}{0pt plus 2pt minus 2pt}

\RequirePackage{times} %Tekst on Times tüüpi
\RequirePackage{fancyhdr} %Võimaldab kasutada päiseid ja jaluseid
\setlength{\parindent}{0cm} %Lõigu taane on seatud nulliks


\RequirePackage{setspace} %Vajalik teksti vahede seadistamiseks
\onehalfspacing %Ridade vahel on 1,5 tähe kõrgusest

\setlength{\parskip}{12 pt} %Lõikude vaheline kaugus üksteisest

\newcommand{\blank}[1]{\hspace*{#1}} %Luuakse käsk "blank", mille parameeter cm'ides loob taande vasakult servast

\hyphenation{põhi-tekstis üliõpilas-kood lehe-küljed joonda-takse} %Ebakorrektse poolitamise parandamine

\renewcommand{\arraystretch}{1.15} %Tabelis olev reavahe

\setlength{\footskip}{0pt} %Pole kindel, aga peaks vähendama lk numbri vahelist kaugust alaservast

\newenvironment{CenteredBox}{% 
\begin{Sbox}}{% Save the content in a box
\end{Sbox}\centerline{\parbox{\wd\@Sbox}{\TheSbox}}}% And output it centered

\RequirePackage[acronym,nohypertypes={acronym,notation}]{glossaries}

\graphicspath{{figures//}}

% Code to be executed after laTeX has processed
% the begin document tag
\AtBeginDocument{
  \normalfont   % Select the normal font
  \normalsfcodes % To correct spacing in headers
  \makeindex
}