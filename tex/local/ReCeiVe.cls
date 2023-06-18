%% ReCeiVe CV Class File
%
% Author:
% Alex Erdin <alexerdin@outlook.com>
% Based on the template by Claud D. Park <posquit0.bj@gmail.com>
%-------------------------------------------------------------------------------
%				 Identification
%-------------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ReCeiVe}[2020/10/10 v1.1 ReCeiVe Curriculum Vitae Class]

%-------------------------------------------------------------------------------
%				 Class options
%-------------------------------------------------------------------------------
% Options for draft or final
\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption{leftPos}{\def\@sidebarPos{left}}
\DeclareOption{rightPos}{\def\@sidebarPos{right}}

% Inherit options of article
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

%-------------------------------------------------------------------------------
%				 General packages
%-------------------------------------------------------------------------------
% Configure page layout
\RequirePackage{geometry}
% To change section styles (explicit)
\RequirePackage[explicit]{titlesec}
% Needed to make header & footer effeciently
\RequirePackage{fancyhdr}
% Needed to handle text alignment
\RequirePackage{ragged2e}
% Toolbox of programming tools
\RequirePackage{etoolbox}
% Change line spacing in specific environment
\RequirePackage{setspace}
% Manage colors
\RequirePackage{xcolor}
% Ad pictures
\RequirePackage{graphicx}
% Create a background, sidebar, ect.
\RequirePackage{tikz}
% Change date format
\RequirePackage[yyyymmdd]{datetime}
% Handle list environments
\RequirePackage{enumitem}
% Make fixed length table
\RequirePackage{array}
% Deal with hyperlinks
\RequirePackage[hidelinks]{hyperref}
% Assigne LaTeX macros with optional arguments
\RequirePackage{letltxmacro}
% Calculate new values on the go
\RequirePackage{calc}

%-------------------------------------------------------------------------------
%				Layout configurations
%-------------------------------------------------------------------------------
%% Page Layout
% Preallocate some lengths
\newlength{\@topMarg}
\newlength{\@leftMarg}
\newlength{\@sidebarWidth}
\newlength{\@headerWidth}
\newlength{\acvSidebarSep}
\setlength{\acvSidebarSep}{5mm}
% Redefine geometry macro
\LetLtxMacro{\oldgeometry}{\geometry}
\renewcommand{\geometry}[2][6cm]{\oldgeometry{#2}
	\setlength{\@headerWidth}{\textwidth}
	\setlength{\@leftMarg}{1in+\hoffset+\oddsidemargin}
	\setlength{\@topMarg}{1in+\voffset+\topmargin+\headheight+\headsep}

	\ifthenelse{\isundefined{\@sidebarPos}}{
		\ClassWarning{ReCeiVe}{Class option "sidebarPos" is undefined, use leftPos or rightPos to specify the sidebar position.}
	}{%
		\setlength{\@sidebarWidth}{#1}
		\addtolength{\textwidth}{-#1-\acvSidebarSep}
		\ifthenelse{\equal{\@sidebarPos}{left}}{%
			\addtolength{\oddsidemargin}{#1+\acvSidebarSep}
			\addtolength{\evensidemargin}{#1+\acvSidebarSep}
		}{}
	}
}
% Configure page margins with geometry
\geometry{left=1.75cm, right=1.75cm, top=1.5cm, bottom=1.5cm, footskip=.6cm, headsep=.5cm}% margins
% Remove indent
\setlength{\parindent}{0pt}

%% Header & Footer
% Set offset to each header and footer
\fancyhfoffset{0em}
% Remove head rule
\renewcommand{\headrulewidth}{0pt}
% Clear all header & footer fields
\fancyhf{}
% Enable to make header or footer using fancyhdr
\pagestyle{fancy}

%-------------------------------------------------------------------------------
%				Color configurations
%-------------------------------------------------------------------------------
% Gray-scale colors
\definecolor{darkgray}{HTML}{333333}
\definecolor{gray}{HTML}{5D5D5D}
\definecolor{lightgray}{HTML}{D4D4D4}

% Text colors
\definecolor{darktext}{HTML}{414141}
\colorlet{text}{darkgray}
\colorlet{graytext}{gray}
\colorlet{lighttext}{lightgray}

% Highlight colors
\definecolor{lightblue}{HTML}{B6D0F0}
\definecolor{orange}{HTML}{F0D4B6}
\definecolor{red}{HTML}{F0B6B6}
\definecolor{concrete}{HTML}{BECDCF}
\colorlet{highlight}{lightblue}

%-------------------------------------------------------------------------------
%				 Fonts
%-------------------------------------------------------------------------------
% Manage fonts
\RequirePackage[quiet]{fontspec}
\RequirePackage{raleway}
\RequirePackage{roboto}
\RequirePackage[default,opentype]{sourcesanspro}
% Icons from font-awesome
\RequirePackage{fontawesome}

% Set default sans-serife
\renewcommand*\familydefault{\sfdefault}
%Set header font
\newfontfamily\headerfont[%
  UprightFont=*-Regular,
  ItalicFont=*-Italic,
  BoldFont=*-Bold,
  BoldItalicFont=*-BoldItalic,
  ]{raleway}

% Set font for body and footer
\newcommand*{\bodyfont}{\sourcesanspro}
\newcommand*{\bodyfontlight}{\sourcesansprolight}
\newcommand*{\footerfont}{\sourcesanspro}

% Icon with text
% Usage: \icon[framed|unframed]{<size>}{<icon>}{<text>}
\newcommand{\icon}[4][framed]{%
	\ifthenelse{\equal{#1}{framed}}{%
	\vcenteredhbox{\colorbox{black}{\makebox(#2, #2){\textcolor{highlight}{\large\csname fa#3\endcsname}}}}% Icon and box
	\acvHeaderIconSep\headersocialstyle{#4}%
	}{%
	\ifthenelse{\equal{#1}{unframed}}{
		\csname fa#3\endcsname\acvHeaderIconSep\headersocialstyle{#4}%
		}{%
		\ClassWarning{ReCeiVe}{Unknown option for icon is used. Available options are: framed | unframed}%
		}
	}
}

% Command to vertically centre adjacent content
\newcommand{\vcenteredhbox}[1]{% The only parameter is for the content to centre
	\begingroup%
		\setbox0=\hbox{#1}\parbox{\wd0}{\box0}%
	\endgroup%
}

%-------------------------------------------------------------------------------
%				Styles
%-------------------------------------------------------------------------------
% Configure styles for each CV elements
% Define black framed title style
% Usage: \titlestyle[<baselineskip>]{<fontsize>}{<title>}
\newcommand*{\@titlestyle}[3][1em]{\colorbox{black}{\fontsize{#2}{#1}\headerfont\bfseries\textcolor{highlight}{\MakeUppercase{#3}}}}

% Header styles
\newcommand*{\headerlastnamestyle}[1]{\@titlestyle{30pt}{#1}}
\newcommand*{\headerfirstnamestyle}[1]{{\fontsize{30pt}{1em}\headerfont #1}}
\newcommand*{\headerpositionstyle}[1]{{\fontsize{18pt}{1em}\bodyfont\color{text} #1}}
\newcommand*{\headwordsstyle}[1]{{\fontsize{8pt}{1em}\headerfont\itshape\color{darktext} #1}}
\newcommand*{\headersocialstyle}[1]{{\fontsize{10pt}{1em}\headerfont\color{text} #1}}
\newcommand*{\headerquotestyle}[1]{{\fontsize{9pt}{1em}\bodyfont\itshape\color{darktext} #1}}
\newcommand*{\footerstyle}[1]{{\fontsize{8pt}{1em}\footerfont\scshape\color{lighttext} #1}}

% Section styles
\newcommand*{\sectionstyle}[1]{\@titlestyle[1em]{15pt}{#1}}

% For elements of entry
\newcommand*{\entrytitlestyle}[1]{{\fontsize{10pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\entrypositionstyle}[1]{{\fontsize{8pt}{1em}\bodyfont\scshape\color{graytext} #1}}
\newcommand*{\entrydatestyle}[1]{{\fontsize{8pt}{1em}\bodyfontlight\slshape\color{graytext} #1}}
\newcommand*{\entrylocationstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\slshape\color{text} #1}}
\newcommand*{\entryitemstyle}{\fontsize{9pt}{1em}\bodyfontlight\upshape\color{text}}

% For elements of honor
\newcommand*{\honortitlestyle}[1]{{\fontsize{9pt}{1em}\bodyfont\color{graytext} #1}}
\newcommand*{\honorpositionstyle}[1]{{\fontsize{9pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\honordatestyle}[1]{{\fontsize{9pt}{1em}\bodyfont\color{graytext} #1}}
\newcommand*{\honorlocationstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\slshape\color{text} #1}}

% For elements of sidebar
\newcommand*{\sidebarstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\upshape\color{text} #1}}
\newcommand*{\skillsetstyle}[1]{{\fontsize{10pt}{1em}\bodyfont\color{darktext} #1}}
\newcommand*{\languagestyle}[1]{{\fontsize{10pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\levelstyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\color{text} #1}}

% For elements of the cover letter
\newcommand*{\lettersectionstyle}[1]{{\fontsize{14pt}{1em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\recipienttitlestyle}{\fontsize{11pt}{1em}\bodyfont\scshape\color{graytext}}
\newcommand*{\lettertitlestyle}[1]{{\fontsize{12pt}{1em}\bodyfontlight\bfseries\color{darktext} #1}}
\newcommand*{\letterdatestyle}[1]{{\fontsize{9pt}{1em}\bodyfontlight\slshape\color{graytext} #1}}
\newcommand*{\lettertextstyle}{\fontsize{10pt}{1.4em}\bodyfontlight\upshape\color{text}}
\newcommand*{\letternamestyle}[1]{{\fontsize{10pt}{1em}\bodyfont\bfseries\color{darktext} #1}}
\newcommand*{\letterenclosurestyle}[1]{{\fontsize{10pt}{1em}\bodyfontlight\slshape\color{graytext} #1}}

%% Redefine section and subsection
%\titleformat{<command>}[<shape>]{<format>}{<label>}{<sep>}{<before-code>}[<after-code>]
\titleformat{\section}[hang]{}{\sectionstyle{#1}}{0pt}{}
%\titlespacing*{<command>}{<left margin>}{<before-sep>}{<after-sep>}
\titlespacing*{\section}{0pt}{\acvSectionTopSkip plus .1ex minus .1ex}{0pt}

% Subsection style
\titleformat{\subsection}[hang]{}{\subsectionstyle{#1}}{0pt}{\vspace{-3mm}}
\titlespacing*{\subsection}{0pt}{\acvSectionContentTopSkip plus .1ex minus .1ex}{0pt}

%-------------------------------------------------------------------------------
%				Commands for control
%-------------------------------------------------------------------------------

%% Define helper macros a user can change easily
% Header
\newcommand{\acvHeaderIconSize}{12}
\newcommand{\acvHeaderIconSep}{\enspace}
\newcommand{\acvHeaderNameDelim}{\space}
\newcommand{\acvHeaderAfterNameSkip}{2mm}
\newcommand{\acvHeaderAfterPositionSkip}{.4mm}
\newcommand{\acvHeaderAfterHeadwordsSkip}{.5mm}
\newcommand{\acvHeaderSocialSep}{\enspace\textbar\enspace}
\newcommand{\acvHeaderAfterSocialSkip}{4mm}
\newcommand{\acvHeaderAfterHeaderSkip}{5mm}
% Sidebar
\newlength{\acvSidebarInnerSep}
\setlength{\acvSidebarInnerSep}{5mm}
\newcommand{\acvSidebarLanguageSep}{\enspace\textbullet\enspace}

% Others
\newcommand{\acvSectionTopSkip}{3mm}
\newcommand{\acvSectionContentTopSkip}{2.5mm}

% Cover letter
\newcommand{\acvSignatureSkip}{20pt}

%-------------------------------------------------------------------------------
%				Commands for utility
%-------------------------------------------------------------------------------

%% Define some macros for usage
% Define commands for tabular environment
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

% Define command for automatic setting of delimeters
% Usage: \@setdelim{<delim1>}{<delim2>}
\newbool{startflag}
\newbool{delimflag}
\newcommand*{\@setdelim}[2]{%
	\ifbool{startflag}{%
		\ifbool{delimflag}{%
			#1%
			\global\boolfalse{delimflag}%
		  }{%
			#2%
			\global\booltrue{delimflag}%
		  }%
	  }{%
		\global\booltrue{startflag}%
		\global\booltrue{delimflag}%
	  }%
	\ignorespaces%
}

% Redefine list environments
\setlist[itemize]{leftmargin=3ex, nosep, itemsep=1ex, label=\bullet}

%-------------------------------------------------------------------------------
%				Commands for personal information
%-------------------------------------------------------------------------------
% Define photo ID
% Usage: \photo[circle|rectangle,edge|noedge,fill|nofill,left|right]{size,<path-to-image>}
\newlength{\@photosize}
\newcommand{\photo}[3][circle,edge,left]{%
  \setlength{\@photosize}{#2}\def\@photo{#3}%
  \@for\tmp:=#1\do{%
	\ifthenelse{\equal{\tmp}{circle} \or \equal{\tmp}{rectangle}}%
	  {\let\@photoshape\tmp}{}%
	\ifthenelse{\equal{\tmp}{edge} \or \equal{\tmp}{noedge}}%
	  {\let\@photoedge\tmp}{}%
	\ifthenelse{\equal{\tmp}{fill} \or \equal{\tmp}{nofill}}%
	  {\let\@photofill\tmp}{}%
	\ifthenelse{\equal{\tmp}{left} \or \equal{\tmp}{right}}%
	  {\let\@photoalign\tmp}{}%
  }%
}
\def\@photoshape{circle}
\def\@photoedge{edge}
\def\@photofill{fill}
\def\@photoalign{left}

% Define background from picture library (optional)
% Usage: \background{<pics/pic>}
\newcommand*{\background}[1]{\def\@background{#1}}

% Define about me section (optional)
% Usage: \aboutMe{<content>}
\newcommand*{\aboutMe}[2][About Me]{\def\@aboutMetitle{#1}\def\@aboutMe{#2}}

% Define a command for printing skill progress bars (optional)
% Usage: \skillset[title/value,label/value]{<label1/grade1>,<label2/grade2>, ect.}
\newcommand*{\skillset}[2][]{%
	% Get optional arguments
	\def\@skillstitle{Skills}
	%\def\@skillslabel{}
	\foreach \argName/\value in {#1}{%
		\ifthenelse{\equal{\argName}{title}}{%
			\xdef\@skillstitle{\value}}{}%
		\ifthenelse{\equal{\argName}{label}}{%
			\xdef\@skillslabel{\value}}{}%
	}%
	%\def\@skillstitle{Skill}
	\providecommand*{\skills}{}
	\renewcommand*{\skills}[1]{%
		\begin{tikzpicture}
			\foreach [count=\i] \skilllabel/\skillvalue in {#2}{%
				\fill [white] (0,\i) rectangle (##1,\i+0.4);
				\fill [gray](0,\i) rectangle (\skillvalue*##1,\i+0.4);
				\node [above right] at (0,\i+0.4) {\skilllabel};
			}
		\end{tikzpicture}
	}
}

% Define a command for printing language skills (optional)
% Usage: \languages{{<language1/level1>},{<language2/level2>}, ect.}
\newcommand*{\languages}[2][Languages]{%
	\def\@languagestitle{#1}
	\providecommand*{\@languagesContent}{%
		\foreach \language/\level in {#2}{%
   			\languagestyle{\language}\@ \acvSidebarLanguageSep \levelstyle{\level} \par
		}
	}
}

% Define hobbies section (optional)
% Usage: \hobbies{<content>}
\newcommand*{\hobbies}[2][Hobbies]{\def\@hobbiestitle{#1}\def\@hobbies{#2}}

% Define non profit section (optional)
% Usage: \nonProfit{<content>}
\newcommand*{\nonProfit}[2][Non Profit]{\def\@nonProfittitle{#1}\def\@nonProfit{#2}}

% Define user-section (optional)
% Usage: \usersection[<title>]{<content>}
\newcommand*{\userSection}[2][]{\def\@userTitle{#1}\def\@userContent{#2}}

% Define writer's name
% Usage: \name{<firstname>}{<lastname>}
% Usage: \firstname{<firstname>}
% Usage: \lastname{<lastname>}
% Usage: \familyname{<familyname>}
\newcommand*{\name}[2]{\def\@firstname{#1}\def\@lastname{#2}}
\newcommand*{\firstname}[1]{\def\@firstname{#1}}
\newcommand*{\lastname}[1]{\def\@lastname{#1}}
\newcommand*{\familyname}[1]{\def\@lastname{#1}}
\def\@familyname{\@lastname}

% Define writer's position (optional)
% Usage: \name{<position>}
\newcommand*{\position}[1]{\def\@position{#1}}

% Define writer's address (optional)
% Usage: \address{<address>}
\newcommand*{\address}[1]{\def\@address{#1}}

% Defines writer's mobile (optional)
% Usage: \mobile{<mobile number>}
\newcommand*{\mobile}[1]{\def\@mobile{#1}}

% Defines writer's email (optional)
% Usage: \email{<email adress>}
\newcommand*{\email}[1]{\def\@email{#1}}

% Defines writer's homepage (optional)
% Usage: \homepage{<url>}
\newcommand*{\homepage}[1]{\def\@homepage{#1}}

% Defines writer's linked-in (optional)
% Usage: \linkedin{<linked-in-nick>}
\newcommand*{\linkedin}[1]{\def\@linkedin{#1}}

% Usage: \twitter{<twitter handle>}
\newcommand*{\twitter}[1]{\def\@twitter{#1}}

% Defines writer's xing (optional)
% Usage: \xing{<xing name>}
\newcommand*{\xing}[1]{\def\@xing{#1}}

% Defines writer's github (optional)
% Usage: \github{<github-nick>}
\newcommand*{\github}[1]{\def\@github{#1}}

% Defines writer's gitlab (optional)
% Usage: \gitlab{<gitlab-nick>}
\newcommand*{\gitlab}[1]{\def\@gitlab{#1}}

% Defines writer's stackoverflow profile (optional)
% Usage: \stackoverflow{<so userid>}{<so username>}
% e.g.https://stackoverflow.com/users/123456/sam-smith
% would be \stackoverflow{123456}{sam-smith}
\newcommand*{\stackoverflow}[2]{\def\@stackoverflowid{#1}\def\@stackoverflowname{#2}}

% Defines writer's skype (optional)
% Usage: \skype{<skype account>}
\newcommand*{\skype}[1]{\def\@skype{#1}}

% Defines writer's reddit (optional)
% Usage: \reddit{<reddit account>}
\newcommand*{\reddit}[1]{\def\@reddit{#1}}

% Defines writer's extra informations (optional)
% Usage: \extrainfo{<extra informations>}
\newcommand*{\extrainfo}[1]{\def\@extrainfo{#1}}

% Defines few headwords (optional)
% Usage: \headwords{<headwords>}
\newcommand*{\headwords}[1]{\def\@headwords{#1}}

% Defines writer's quote (optional)
% Usage: \quote{<quote>}
\renewcommand*{\quote}[1]{\def\@quote{#1}}

% Defines recipient's information (cover letter only, optional)
% Usage: \recipient{<recipient name>}{<recipient street>}{<recipient town>}{<recipient phone>}
% Usage: \recipientname{<recipient name>}
% Usage: \recipientstreet{<recipient street>}
% Usage: \recipienttown{<recipient town>}
% Usage: \recipientphone{<recipient phone>}
\newcommand*{\recipient}[5][]{\def\@recipientname{#2}\def\@recipientcompany{#3}\def\@recipientstreet{#4}\def\@recipienttown{#5}\def\@recipientphone{#1}}
\newcommand*{\recipientname}[1]{\def\@recipientname{#1}}
\newcommand*{\recipientcompany}[1]{\def\@recipientcompany{#1}}
\newcommand*{\recipientstreet}[1]{\def\@recipientstreet{#1}}
\newcommand*{\recipienttown}[1]{\def\@recipienttown{#1}}
\newcommand*{\recipientphone}[1]{\def\@recipientphone{#1}}

% Defines the title for letter (cover letter only, optional)
% Usage: \lettertitle{<title>}
\newcommand*{\lettertitle}[1]{\def\@lettertitle{#1}}

% Defines the date for letter (cover letter only)
% Usage: \letterdate{<date>}
\newcommand*{\letterdate}[1][\today{}]{\def\@letterdate{#1}}
\letterdate

% Defines a message of opening for letter (cover letter only)
% Usage: \letteropening{<message>}
\newcommand*{\letteropening}[1]{\def\@letteropening{#1}}

% Defines a message of closing for letter (cover letter only)
% Usage: \letterclosing{<message>}
\newcommand*{\letterclosing}[1]{\def\@letterclosing{#1}}

% Defines an enclosure for letter (cover letter only, optional)
% Usage: \letterenclosure[<enclosure name>]{<enclosure>}
\newcommand*{\letterenclosure}[2][Enclosure]{\def\@letterenclname{#1}\def\@letterenclosure{#2}}

%-------------------------------------------------------------------------------
%				Commands for CV structure
%-------------------------------------------------------------------------------

% Draw CV background
% Usage: \drawbackground[<opacity>]
\newcommand*{\drawbackground}[1][0.15]{%
	\ifthenelse{\isundefined{\@background}}{%
	}{%
		\begin{tikzpicture}[remember picture,overlay]%
			{\node[opacity=#1] at (current page.center)%
			{\includegraphics[width=\paperwidth,height=\paperheight]{\@background}};}%
		\end{tikzpicture}%
	}%
}

% Define a header for CV
% Usage: \makecvheader[<left|center>]
\newcommand*{\makecvheader}[1][L]{%
	\newcommand*{\drawphoto}{%
		\ifthenelse{\isundefined{\@photo}}
			{}{%
			\newlength{\@edgeradius}
			\newlength{\@photowidth}
			\ifthenelse{\equal{\@photoshape}{circle}}{%
				\setlength{\@photowidth}{\@photosize}
				\setlength{\@edgeradius}{0cm}}{%
				\settowidth{\@photowidth}{\includegraphics[height=\@photosize]{\@photo}}
				\setlength{\@edgeradius}{0.2\@photosize}}%
			\ifthenelse{\equal{\@photoedge}{edge}}{%
				\def\@photoborder{darkgray}}{%
				\def\@photoborder{none}}%
			\ifthenelse{\equal{\@photofill}{fill}}{%
				\def\@photofillcolor{highlight}}{%
				\def\@photofillcolor{none}}%
			\begin{tikzpicture}
			\node [\@photoshape, draw=\@photoborder, fill=\@photofillcolor, line width=0.3mm, minimum height = \@photosize,
				  minimum width=\@photowidth, rounded corners=\@edgeradius,
				  path picture ={\node [xshift=0cm, yshift=0cm] at (path picture bounding box.center)
				  {\includegraphics[height=\@photosize]{\@photo}};
				}]{};
			\end{tikzpicture}
		}
	}
	%
	\newcommand*{\@headersocial}[3][unframed]{%
		\global\boolfalse{startflag}% reset startflag
		\ifthenelse{\isundefined{\@address}}%
			{}{%
			\@setdelim{##2}{##3}%
			\icon[##1]{\acvHeaderIconSize}{MapMarker}{\@address}%
		}%
		\ifthenelse{\isundefined{\@mobile}}%
			{}{%
			\@setdelim{##2}{##3}%
			\icon[##1]{\acvHeaderIconSize}{Mobile}{\@mobile}%
		}%
		\ifthenelse{\isundefined{\@email}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{mailto:\@email}{\icon[##1]{\acvHeaderIconSize}{Envelope}{\@email}}%
		}%
		\ifthenelse{\isundefined{\@homepage}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{http://\@homepage}{\icon[##1]{\acvHeaderIconSize}{Home}{\@homepage}}%
		}%
		\ifthenelse{\isundefined{\@linkedin}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{https://www.linkedin.com/in/\@linkedin}{\icon[##1]{\acvHeaderIconSize}{Linkedin}{\@linkedin}}%
		}%
		\ifthenelse{\isundefined{\@twitter}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{https://twitter.com/\@twitter}{\icon[##1]{\acvHeaderIconSize}{Twitter}{\@twitter}}%
		}%
		\ifthenelse{\isundefined{\@xing}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{https://www.xing.com/profile/\@xing}{\icon[##1]{\acvHeaderIconSize}{XingSquare}{\@xing}}%
		}%
		\ifthenelse{\isundefined{\@github}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{https://github.com/\@github}{\icon[##1]{\acvHeaderIconSize}{GithubSquare}{\@github}}%
		}%
		\ifthenelse{\isundefined{\@gitlab}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{https://gitlab.com/\@gitlab}{\icon[##1]{\acvHeaderIconSize}{Gitlab}{\@gitlab}}%
		}%
	  \ifthenelse{\isundefined{\@stackoverflowid}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{https://stackoverflow.com/users/\@stackoverflowid}{\icon[##1]{\acvHeaderIconSize}{StackOverflow}{\@stackoverflowname}}%
		}%
		\ifthenelse{\isundefined{\@skype}}%
			{}{%
			\@setdelim{##2}{##3}%
			\icon[##1]{\acvHeaderIconSize}{Skype}{\@skype}%
		}%
		\ifthenelse{\isundefined{\@reddit}}%
			{}{%
			\@setdelim{##2}{##3}%
			\href{https://www.reddit.com/user/\@reddit}{\icon[##1]{\acvHeaderIconSize}{Reddit}{\@reddit}}%
		}%
		\ifthenelse{\isundefined{\@extrainfo}}%
			{}{%
			\@setdelim{##2}{##3}%
			\@extrainfo%
		}%
	}
	%
	% Initialize lengths
	\newlength{\@headerheight}
	\newlength{\@headertextwidth}
	\newlength{\@headerleftbox}
	\newlength{\@headerrightbox}
	% Set lengths
	\setlength{\@headertextwidth}{\@headerWidth}%
	\ifthenelse{\equal{#1}{L}}{%
		\setlength{\@headertextwidth}{0.4\@headerWidth}%
		\setlength{\@headerrightbox}{0.6\@headerWidth}%
		}{%
		\ifthenelse{\isundefined{\@photo}}{%
			}{%
			\addtolength{\@headertextwidth}{-\@photosize}%
			\ifthenelse{\equal{\@photoalign}{left}}{%
				\setlength{\@headerleftbox}{\@photosize}%
				}{%
				\setlength{\@headerrightbox}{\@photosize}%
			}
		}
	}
	% Save cv header with sbox
	\newsavebox{\headerbox}
	\sbox{\headerbox}{%
	\begin{minipage}[c]{\@headertextwidth}
		\ifthenelse{\equal{#1}{L}}{% Left
			\raggedright%
			\headerlastnamestyle{\@firstname}\\%
			\headerlastnamestyle{\@lastname}%
			\\[\acvHeaderAfterNameSkip]%
			\ifthenelse{\isundefined{\@position}}{}{\headerpositionstyle{\@position}}\\%
			\vspace{\acvHeaderAfterHeaderSkip}%
		}{%
			\ifthenelse{\equal{#1}{C}}{% Center
			\centering%
			\headerfirstnamestyle{\@firstname{}\acvHeaderNameDelim}\headerlastnamestyle{\@lastname}%
			\\[\acvHeaderAfterNameSkip]%
			\ifthenelse{\isundefined{\@position}}{}{\headerpositionstyle{\@position\\[\acvHeaderAfterPositionSkip]}}%
			\ifthenelse{\isundefined{\@headwords}}{}{\headwordsstyle{\@headwords\\[\acvHeaderAfterHeadwordsSkip]}}%
			\@headersocial{\acvHeaderSocialSep}{\acvHeaderSocialSep}%
			\ifthenelse{\isundefined{\@quote}}{%
				\\[\acvHeaderAfterHeaderSkip]%
				}{%
				\\[\acvHeaderAfterSocialSkip]
				\headerquotestyle{\@quote\\}\vspace{\acvHeaderAfterHeaderSkip}}%
		}{% Else
			\ClassWarning{ReCeiVe}{Unknown option for makecvheader is used. Available options are: L | C}
		}
	}
	\end{minipage}%
	}
	% Measure cv header height
	\setlength{\@headerheight}{\ht\headerbox+\dp\headerbox}
	%
	% Set makebox position
	\ifthenelse{\isundefined{\@sidebarPos}}{%
		\def\@boxPos{c}
		}{%
		\ifthenelse{\equal{\@sidebarPos}{left}}{%
			\def\@boxPos{r}
			}{%
			\def\@boxPos{l}
		}
	}
	% Draw cv background
	\drawbackground%
	%
	% Draw entire cv header
	\makebox[\textwidth][\@boxPos]{\makebox[\@headerWidth]{%
	%
	\begin{minipage}[c]{\@headerleftbox}%
		\ifthenelse{\equal{\@photoalign}{left}}{%
			\ifthenelse{\equal{#1}{C}}{%
			\raggedright\drawphoto
			}{}
		}{}
	\end{minipage}
	\usebox{\headerbox}
	\begin{minipage}[c]{\@headerrightbox}%
	  	\ifthenelse{\equal{#1}{L}}{%
		\raggedleft%
		\boolfalse{startflag}%
		\setlength{\extrarowheight}{\acvHeaderIconSize pt}%
		\begin{tabular}{l  l}
			\@headersocial[framed]{&}{\\}%
		\end{tabular}
		}{%
		\ifthenelse{\equal{\@photoalign}{right}}{%
			\ifthenelse{\equal{#1}{C}}{%
			\raggedleft\drawphoto
			}{}
		}{}
	}
	\end{minipage}
	}}
}

% Usage: \makecvsidebar[xOffset/value,yOffset/value,noRadius|radius]
\newcommand*{\makecvsidebar}[1][]{%
	\ifthenelse{\isundefined{\@headerheight}}{%
		\ClassWarning{ReCeiVe}{Warning: headerheight is undefined. Use makecvheader before using makecvsidebar.}%
	}{%
		\ifthenelse{\isundefined{\@sidebarPos}}{%
		}{%  Create lengths
			\newlength{\@xOffset}
			\newlength{\@yOffset}
			\newlength{\@corner}
			\newlength{\@xPosSidebar}
			\newlength{\@yPosSidebar}
			\newlength{\@sidebarHeight}
			\newlength{\@textblockWidth}
			\setlength{\@corner}{0.5cm}

			% Get optional arguments
			\foreach \argName/\value in {#1}{%
				\ifthenelse{\equal{\argName}{xOffset}}{%
					\setlength{\global\@xOffset}{\value}}{}%
				\ifthenelse{\equal{\argName}{yOffset}}{%
					\setlength{\global\@yOffset}{\value}}{}%
				\ifthenelse{\equal{\argName}{noRadius}}{%
					\setlength{\global\@corner}{0pt}}{}%
			}%

			% Set lengths
			\setlength{\@sidebarHeight}{\textheight-\@headerheight-\lineskip-\@yOffset}
			\setlength{\@yPosSidebar}{\@topMarg+\@headerheight+\lineskip+\@yOffset}
			\setlength{\@textblockWidth}{\@sidebarWidth-2\acvSidebarInnerSep}
			\ifthenelse{\equal{\@sidebarPos}{left}}{%
				\setlength{\@xPosSidebar}{\@leftMarg+\@xOffset}
			}{%
				\setlength{\@xPosSidebar}{\@leftMarg+\textwidth+\acvSidebarSep+\@xOffset}
			}
			\newsavebox{\sidebarBox}
			\sbox{\sidebarBox}{
			\begin{minipage}[t]{\@textblockWidth}
				\leavevmode % Enter horizontal mode
				\ifthenelse{\isundefined{\@photo}}{%
				}{%
					\ifthenelse{\isundefined{\@edgeradius}}{%
						{\centering\drawphoto\par}
						\vspace{\acvSectionTopSkip}
						}{}
				}
				\ifthenelse{\isundefined{\@aboutMe}}{%
					}{%
					\vspace{-\acvSectionTopSkip}%
					\section{\@aboutMetitle}%
					\vspace{\acvSectionContentTopSkip}%
					{\justify\sidebarstyle{\@aboutMe}\par}%
				}
				\ifthenelse{\isundefined{\skills}}%
					{}{%
					\section{\@skillstitle}%
					\vspace{\acvSectionContentTopSkip}%
					\skillsetstyle{%
					\skills{\@textblockWidth}%
					}%
					\ifthenelse{\isundefined{\@skillslabel}}
					{\vspace{-10pt}
					}{%
					{\sidebarstyle{\@skillslabel}}%
					}%
				}
				\ifthenelse{\isundefined{\@userContent}}%
					{}{%
					\ifthenelse{\equal{\@userTitle}{}}%
						{}{%
						\section{\@userTitle}%
						\vspace{\acvSectionContentTopSkip}%
					}
					{\justify\sidebarstyle{\@userContent}\par}%
				}
				\ifthenelse{\isundefined{\@languagestitle}}%
					{}{%
					\section{\@languagestitle}%
					\vspace{\acvSectionContentTopSkip}%
					\@languagesContent%
				}
				\ifthenelse{\isundefined{\@hobbies}}%
					{}{%
					\section{\@hobbiestitle}%
					\vspace{\acvSectionContentTopSkip}%
					{\justify\sidebarstyle{\@hobbies}\par}%
				}
				\ifthenelse{\isundefined{\@nonProfit}}%
					{}{%
					\section{\@nonProfittitle}%
					\vspace{\acvSectionContentTopSkip}%
					{\justify\sidebarstyle{\@nonProfit}\par}%
				}
			\end{minipage}
			}

			\begin{tikzpicture}[remember picture,overlay]%
				\node [rectangle, fill=lightgray, rounded corners=\@corner, anchor=north west, shift={(\@xPosSidebar,-\@yPosSidebar)}, minimum width=\@sidebarWidth, minimum height=\@sidebarHeight](sidebarBackground) at (current page.north west){};
				\node [anchor=north, yshift=-0.65\acvSidebarInnerSep] at (sidebarBackground.north){\usebox\sidebarBox};%
			\end{tikzpicture}%
		}
	}
}

% Define a footer for CV
% Usage: \makecvfooter{<left>}{<center>}{<right>}
\newcommand*{\makecvfooter}[3]{%
	\fancyfoot{}

	% Set footer position
	\ifthenelse{\isundefined{\@sidebarPos}}{%
		\fancyfoot[L]{\footerstyle{\raggedright#1}}
		\fancyfoot[C]{\footerstyle{\centering#2}}
		\fancyfoot[R]{\footerstyle{\raggedleft#3}}
		}{%
		% Create saveboxes
		\newsavebox{\@leftFoot}
		\newsavebox{\@centerFoot}
		\newsavebox{\@rightFoot}
		\newsavebox{\@footerBox}
		\sbox{\@leftFoot}{#1}
		\sbox{\@centerFoot}{#2}
		\sbox{\@rightFoot}{#3}

		% Get savebox widths
		\newdimen\@leftFootwd
		\newdimen\@centerFootwd
		\newdimen\@rightFootwd
		\@leftFootwd = \wd\@leftFoot
		\@centerFootwd = \wd\@centerFoot
		\@rightFootwd = \wd\@rightFoot

		% Calculate minipage widths
		\ifdim \@leftFootwd > \@rightFootwd%
			\ifdim \@centerFootwd > \dimexpr\@headerWidth-2\@leftFootwd\relax%
				\@rightFootwd = \dimexpr\@headerWidth-\@leftFootwd\relax
				\@centerFootwd = 0pt
				\ClassWarning{ReCeiVe}{Left footer is too large, therefore centered footer was omitted.}
			\else%
				\@rightFootwd = \@leftFootwd
				\@centerFootwd = \dimexpr\@headerWidth-2\@leftFootwd\relax
			\fi
		\else%
			\ifdim \@centerFootwd > \dimexpr\@headerWidth-2\@rightFootwd\relax%
				\@leftFootwd = \dimexpr\@headerWidth-\@rightFootwd\relax
				\@centerFootwd = 0pt
				\ClassWarning{ReCeiVe}{Right footer is too large, therefore centered footer was omitted.}
			\else%
				\@leftFootwd = \@rightFootwd
				\@centerFootwd = \dimexpr\@headerWidth-2\@rightFootwd\relax
			\fi
		\fi

		% Creat footer box
		\savebox{\@footerBox}[\@headerWidth]{%
			\footerstyle{%
			\begin{minipage}[t]{\@leftFootwd}
				\ifdim \@leftFootwd > 0pt%
					\ifdim 0pt = \wd\@leftFoot%
						\,%
					\else
						\raggedright#1%
					\fi
				\fi
			\end{minipage}
			\begin{minipage}[t]{\@centerFootwd}
				\ifdim \@centerFootwd > 0pt%
					\ifdim 0pt = \wd\@centerFoot%
						\,%
					\else
						\centering#2%
					\fi
				\fi
			\end{minipage}
			\begin{minipage}[t]{\@rightFootwd}
				\ifdim \@rightFootwd > 0pt%
					\ifdim 0pt = \wd\@rightFoot%
						\,%
					\else
						\raggedleft#3%
					\fi
				\fi
			\end{minipage}
			}
		}

		\ifthenelse{\equal{\@sidebarPos}{left}}{%
			\fancyfoot[R]{% Print usebox
				\makebox[\textwidth][r]{\usebox{\@footerBox}}
			}}{%
			\fancyfoot[L]{% Print usebox
				\makebox[\textwidth][l]{\usebox{\@footerBox}}
			}
		}
	}
}

%-------------------------------------------------------------------------------
%				Environments for CV structure
%-------------------------------------------------------------------------------

% Define an environment for cventries
\newenvironment{cventries}{%
  \begin{flushleft}
}{%
  \end{flushleft}
}
% Define an entry of cv information
% Usage: \cventry{<position>}{<title>}{<location>}{<date>}
\newcommand*{\cventry}[4]{%
	\vspace{\acvSectionContentTopSkip}%
	\ifthenelse{\equal{#2#3}{}}{%
		\entrypositionstyle{#1} \hfill \entrydatestyle{#4}\par
		}{%
		\entrytitlestyle{#2}	\hfill \entrylocationstyle{#3}\par
		\entrypositionstyle{#1} \hfill \entrydatestyle{#4}\par
	}
}

% Define an environment for cvhonor
\newenvironment{cvhonors}{%
	\vspace{\acvSectionContentTopSkip}%
	\begin{flushleft}
		\setlength\tabcolsep{0pt}%
		\setlength{\extrarowheight}{0pt}%
		\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} C{1.5cm} L{\textwidth - 4.0cm} R{2.5cm}}
}{%
		\end{tabular*}
	\end{flushleft}
}
% Define a line of cv information(honor, award or something else)
% Usage: \cvhonor{<position>}{<title>}{<location>}{<date>}
\newcommand*{\cvhonor}[4]{%
  \honordatestyle{#4} & \honorpositionstyle{#1}, \honortitlestyle{#2} & \honorlocationstyle{#3} \\
}

% Define an environment for cvitems(for cventry)
\newenvironment{cvitems}{%
	\vspace{-2.0mm}%
	\begin{justify}
	\entryitemstyle
	\begin{itemize}[noitemsep]
		\setlength{\parskip}{0pt}

}{%
	\end{itemize}
	\end{justify}
	\vspace{-4.0mm}
}

%-------------------------------------------------------------------------------
%                Commands for Cover Letter Structure
%-------------------------------------------------------------------------------
% Define a title of the cover letter
% Usage: \makelettertitle[L|R]
\newcommand*{\makelettertitle}[1][L]{%
	\ifthenelse{\equal{#1}{L}}{%
		\raggedright\\[5mm]
	}{%
		\raggedleft\\[5mm]
	}
	{\recipienttitlestyle
	\ifthenelse{\isundefined{\@recipientname}}{}{\@recipientname\par}
	\ifthenelse{\isundefined{\@recipientcompany}}{}{\@recipientcompany\par}
	\ifthenelse{\isundefined{\@recipientstreet}}{}{\@recipientstreet\par}
	\ifthenelse{\isundefined{\@recipienttown}}{}{\@recipienttown\par}
	\ifthenelse{\isundefined{\@recipientphone}}{}{\@recipientphone\par}
	}
	\raggedright
	\vspace{10pt}
	\letterdatestyle{\@letterdate} \par\smallskip
	\ifthenelse{\isundefined{\@lettertitle}}{}{\lettertitlestyle{\@lettertitle} \\[\acvSectionTopSkip]}
	\ifthenelse{\isundefined{\@letteropening}}{}{\lettertextstyle{\@letteropening} \par\bigskip}
}

% Define a closing of the cover letter
% Usage: \makeletterclosing
\newcommand*{\makeletterclosing}{%
  \vspace{3.5mm}
  \lettertextstyle{\@letterclosing} \\[\acvSignatureSkip]
  \letternamestyle{\@firstname\ \@lastname}
  \ifthenelse{\isundefined{\@letterenclosure}}{}{%
      \\[20pt]
      \letterenclosurestyle{\@letterenclname: \@letterenclosure} \\
    }
}

%-------------------------------------------------------------------------------
%				Environments for Cover Letter
%-------------------------------------------------------------------------------
% Define an environment for cvletter
\newenvironment{cvletter}{%
  \lettertextstyle
}{%
}
