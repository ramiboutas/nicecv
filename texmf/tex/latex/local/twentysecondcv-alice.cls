\ProvidesClass{twentysecondcv}[2017/01/08 CV class]
\LoadClass{article}
\NeedsTeXFormat{LaTeX2e}

%----------------------------------------------------------------------------------------
%	 REQUIRED PACKAGES
%----------------------------------------------------------------------------------------

\RequirePackage[sfdefault]{ClearSans}
\RequirePackage[T1]{fontenc}
\RequirePackage{tikz}
\RequirePackage{xcolor}
\RequirePackage[absolute,overlay]{textpos}
\RequirePackage{ragged2e}
\RequirePackage{etoolbox}
\RequirePackage{ifmtarg}
\RequirePackage{ifthen}
\RequirePackage{pgffor}
\RequirePackage{marvosym}
\RequirePackage{parskip}
\RequirePackage{fontawesome5}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

%----------------------------------------------------------------------------------------
%	 COLOURS
%----------------------------------------------------------------------------------------

\definecolor{white}{RGB}{255,255,255}
\definecolor{gray}{HTML}{4D4D4D}
\definecolor{sidecolor}{HTML}{E7E7E7}
\definecolor{mainblue}{HTML}{0E5484}
\definecolor{maingray}{HTML}{B9B9B9}

%----------------------------------------------------------------------------------------
%	 MISC CONFIGURATIONS
%----------------------------------------------------------------------------------------

\renewcommand{\bfseries}{\color{gray}} % Make \textbf produce coloured text instead

\pagestyle{empty} % Disable headers and footers

\setlength{\parindent}{0pt} % Disable paragraph indentation

%----------------------------------------------------------------------------------------
%	 SIDEBAR DEFINITIONS
%----------------------------------------------------------------------------------------

\setlength{\TPHorizModule}{1cm} % Left margin
\setlength{\TPVertModule}{1cm} % Top margin

\newlength\imagewidth
\newlength\imagescale
\pgfmathsetlength{\imagewidth}{5cm}
\pgfmathsetlength{\imagescale}{\imagewidth/600}

\newlength{\TotalSectionLength} % Define a new length to hold the remaining line width after the section title is printed
\newlength{\SectionTitleLength} % Define a new length to hold the width of the section title
\newcommand{\profilesection}[1]{%
	\setlength\TotalSectionLength{\linewidth}% Set the total line width
	\settowidth{\SectionTitleLength}{\huge #1 }% Calculate the width of the section title
	\addtolength\TotalSectionLength{-\SectionTitleLength}% Subtract the section title width from the total width
	\addtolength\TotalSectionLength{-2.22221pt}% Modifier to remove overfull box warning
	\vspace{8pt}% Whitespace before the section title
	{\color{black!80} \huge #1 \rule[0.15\baselineskip]{\TotalSectionLength}{1pt}}% Print the title and auto-width rule
}

% Define custom commands for CV info
\newcommand{\photo}[1]{\renewcommand{\photo}{#1}}
\newcommand{\fullname}[1]{\renewcommand{\fullname}{#1}}
\newcommand{\jobtitle}[1]{\renewcommand{\jobtitle}{#1}}
\newcommand{\location}[1]{\renewcommand{\location}{#1}}
\newcommand{\birth}[1]{\renewcommand{\birth}{#1}}
\newcommand{\phone}[1]{\renewcommand{\phone}{#1}}
\newcommand{\email}[1]{\renewcommand{\email}{#1}}

\newcommand{\website}[1]{\renewcommand{\website}{#1}}
\newcommand{\linkedin}[1]{\renewcommand{\linkedin}{#1}}
\newcommand{\skype}[1]{\renewcommand{\skype}{#1}}
\newcommand{\instagram}[1]{\renewcommand{\instagram}{#1}}
\newcommand{\twitter}[1]{\renewcommand{\twitter}{#1}}
\newcommand{\facebook}[1]{\renewcommand{\facebook}{#1}}
\newcommand{\youtube}[1]{\renewcommand{\youtube}{#1}}
\newcommand{\github}[1]{\renewcommand{\github}{#1}}
\newcommand{\gitlab}[1]{\renewcommand{\gitlab}{#1}}
\newcommand{\stackoverflow}[1]{\renewcommand{\stackoverflow}{#1}}
\newcommand{\medium}[1]{\renewcommand{\medium}{#1}}
\newcommand{\orcid}[1]{\renewcommand{\orcid}{#1}}

\newcommand{\aboutme}[1]{\renewcommand{\aboutme}{#1}}
\newcommand{\aboutmelabel}[1]{\renewcommand{\aboutmelabel}{#1}}
\newcommand{\skilllabel}[1]{\renewcommand{\skilllabel}{#1}}
\newcommand{\languagelabel}[1]{\renewcommand{\languagelabel}{#1}}

% Command for printing the contact information icons
\newcommand*\icon[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt, fill=mainblue,mainblue,text=white] (char) {#1};}}



\newcommand{\numberofskills}[1]{\renewcommand{\numberofskills}{#1}}

% Command for printing skill progress bars
% \skills{ { Whitespace/5.8}, {good manners/4}, {outgoing/4.3}, {polite/4}, {Java/0.01}}
\newcommand\skills[1]{
	\renewcommand{\skills}{

		\profilesection{ \skilllabel }

		\begin{tikzpicture}
			\foreach [count=\i] \name/\level in {#1}{
				\draw[fill=maingray,maingray] (0,\numberofskills-\i) rectangle (6,\numberofskills-\i+0.4);
				\draw[fill=white,mainblue](0,\numberofskills-\i) rectangle (\level ,\numberofskills-\i+0.4);
				\node [above right] at (0,\numberofskills-\i+0.4) {\name};

			}
		\end{tikzpicture}
	}
}

\newcommand{\numberoflanguages}[1]{\renewcommand{\numberoflanguages}{#1}}

\newcommand\languages[1]{
	\renewcommand{\languages}{

		\profilesection{ \languagelabel }

		\begin{tikzpicture}
		\foreach [count=\i] \name/\level in {#1}{
			\draw[fill=maingray,maingray] (0,\numberoflanguages-\i) rectangle (6,\numberoflanguages-\i+0.4);
			\draw[fill=white,mainblue](0,\numberoflanguages-\i) rectangle (\level ,\numberoflanguages-\i+0.4);
			\node [above right] at (0,\numberoflanguages-\i+0.4) {\name};

		}
		\end{tikzpicture}
	}
}


% Command for printing skills text
\newcommand\skillstext[1]{
	\renewcommand{\skillstext}{
		\begin{flushleft}
			\foreach [count=\i] \x/\y in {#1}{
				\x$ \star $\y
			}
		\end{flushleft}
	}
}

%----------------------------------------------------------------------------------------
%	 SIDEBAR LAYOUT
%----------------------------------------------------------------------------------------

\newcommand{\makeprofile}{
	\begin{tikzpicture}[remember picture,overlay]
   		\node [rectangle, fill=sidecolor, anchor=north, minimum width=9cm, minimum height=\paperheight+1cm] (box) at (-5cm,0.5cm){};
	\end{tikzpicture}

	%------------------------------------------------

	\begin{textblock}{6}(0.5, 0.2)

		%------------------------------------------------

		\ifthenelse{\equal{\photo}{}}{}{
			\begin{center}
				\begin{tikzpicture}[x=\imagescale,y=-\imagescale]
					\clip (600/2, 567/2) circle (567/2);
					\node[anchor=north west, inner sep=0pt, outer sep=0pt] at (0,0) {\photo};
				\end{tikzpicture}
			\end{center}
		}

		%------------------------------------------------

		{\Large\color{mainblue}\fullname}

		%------------------------------------------------

		{\large\color{black!80}\jobtitle}

		%------------------------------------------------

		\renewcommand{\arraystretch}{1.6}
		\begin{tabular}{p{0.5cm} @{\hskip 0.5cm}p{5cm}}
			\ifthenelse{\equal{\location}{}}{}{\textsc{\large\icon{\faMapPin}} & \location\\}
			\ifthenelse{\equal{\birth}{}}{}{\textsc{\large\icon{\faBirthdayCake}} & \birth\\}
			\ifthenelse{\equal{\phone}{}}{}{\textsc{\large\icon{\faMobile*}} & \phone\\}
			\ifthenelse{\equal{\email}{}}{}{\textsc{\large\icon{\faEnvelope[regular]}} & \email\\}
			\ifthenelse{\equal{\website}{}}{}{\textsc{\large\icon{\faGlobeEurope}} & \website\\}
			\ifthenelse{\equal{\linkedin}{}}{}{\textsc{\large\icon{\faLinkedinIn}} & \linkedin\\}
			\ifthenelse{\equal{\skype}{}}{}{\textsc{\large\icon{\faSkype}} & \skype\\}
			\ifthenelse{\equal{\instagram}{}}{}{\textsc{\large\icon{\faInstagram}} & \instagram\\}
			\ifthenelse{\equal{\twitter}{}}{}{\textsc{\large\icon{\faTwitter}} & \twitter\\}
			\ifthenelse{\equal{\facebook}{}}{}{\textsc{\large\icon{\faFacebookF}} & \facebook\\}
			\ifthenelse{\equal{\youtube}{}}{}{\textsc{\large\icon{\faYoutube}} & \youtube\\}
			\ifthenelse{\equal{\github}{}}{}{\textsc{\large\icon{\faGithub}} & \github\\}
			\ifthenelse{\equal{\gitlab}{}}{}{\textsc{\large\icon{\faGitlab}} & \gitlab\\}
			\ifthenelse{\equal{\stackoverflow}{}}{}{\textsc{\large\icon{\faStackOverflow}} & \stackoverflow\\}
			\ifthenelse{\equal{\medium}{}}{}{\textsc{\large\icon{\faMediumM}} & \medium\\}
			\ifthenelse{\equal{\orcid}{}}{}{\textsc{\large\icon{\faOrcid}} & \orcid}
		\end{tabular}

		%------------------------------------------------

		\ifthenelse{\equal{\aboutme}{}}{}{

			\profilesection{ \aboutmelabel }
			\begin{flushleft}
				\aboutme
			\end{flushleft}
		}

		%------------------------------------------------



		\skills
		% \vspace{5mm}
		%\skillstext

		\languages
		\scriptsize
		% (*)[The skill scale is from 0 (Fundamental Awareness) to 6 (Expert).]

		%------------------------------------------------

	\end{textblock}
}

%----------------------------------------------------------------------------------------
%	 COLOURED SECTION TITLE BOX
%----------------------------------------------------------------------------------------

% Command to create the rounded boxes around the first three letters of section titles
\newcommand*\round[2]{%
	\tikz[baseline=(char.base)]\node[anchor=north west, draw,rectangle, rounded corners, inner sep=0.5pt, minimum size=5.5mm, text height=3.6mm, fill=#2,#2,text=white](char){#1};%
}

\newcounter{colorCounter}
\newcommand{\sectioncolor}[1]{%
	{%
		\round{#1}{
			\ifcase\value{colorCounter}%
			maingray\or%
			mainblue\or%
			maingray\or%
			mainblue\or%
			maingray\or%
			mainblue\or%
			maingray\or%
			mainblue\or%
 			maingray\or%
			mainblue\else%
			maingray\fi%
		}%
	}%
	\stepcounter{colorCounter}%
}

\renewcommand{\section}[1]{
	{%
		\color{gray}%
		\Large\sectioncolor{#1}%
	}
}

\renewcommand{\subsection}[1]{
	\par\vspace{.5\parskip}{%
		\large\color{gray} #1%
	}
	\par\vspace{.25\parskip}%
}

%----------------------------------------------------------------------------------------
%	 LONG LIST ENVIRONMENT
%----------------------------------------------------------------------------------------

\setlength{\tabcolsep}{0pt}

% New environment for the long list
\newenvironment{twenty}{%
	\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}ll}
}{%
	\end{tabular*}
}

\newcommand{\twentyitem}[4]{%
	#1&\parbox[t]{0.83\textwidth}{%
		\textbf{#2}%
		\hfill%
		{\footnotesize#3}\\%
		#4\vspace{\parsep}%
	}\\
}

%----------------------------------------------------------------------------------------
%	 SMALL LIST ENVIRONMENT
%----------------------------------------------------------------------------------------

\setlength{\tabcolsep}{0pt}

% New environment for the small list
\newenvironment{twentyshort}{%
	\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}ll}
}{%
	\end{tabular*}
}

\newcommand{\twentyitemshort}[2]{%
	#1&\parbox[t]{0.83\textwidth}{%
		\textbf{#2}%
	}\\
}

%----------------------------------------------------------------------------------------
%	 MARGINS AND LINKS
%----------------------------------------------------------------------------------------

\RequirePackage[left=7.6cm,top=0.1cm,right=1cm,bottom=0.2cm,nohead,nofoot]{geometry}

\RequirePackage{hyperref}
