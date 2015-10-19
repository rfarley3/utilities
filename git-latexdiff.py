#!/usr/bin/env python3
# #############################################
# Nov 2014 rfarley3
#
# Outputs marked up pdf of diff between 2 most
# recent versions of a latex document
# Can handle a document that consists of many tex files
#
# Assumes
#     * '\n' line endings
#     * you only have 1 file with documentclass(call the mainfile)
#          * this is the file you would feed into latex to compile,
#            e.g. pdflatex <mainfile>
#     * you are calling from the dir that contains the mainfile
#     * that the bbl file in the current directory is good enough
#       (so your refs may be wrong)
#     * that your included graphics are either in the current dir or in ../Figs
#
# reimplementation of /opt/local/libexec/git-core/git-latexdiff
# I ran into problems getting git-latexdiff to work
#   specifically it was unable to handle figures in different directories
#   as well as its symlinking method with the current files was
#   not working as expected
#
# TODO:
#    * make repair_graphics generic/customizable
#    * allow arbitrary commit comparisions
#    * make the bbl accurate and diff-able
#
import subprocess
import sys
import os
import os.path
from random import randint

# latex = "latexmk"  # pdflatex"  # alt, use latex = "latexmk"
# latex = "latexmk -pdflatex='pdflatex -file-line-error -interaction=nonstopmode -synctex=1' -pdf"
latex = "latexmk -pdflatex='pdflatex -file-line-error -synctex=1' -pdf"
repair_graphics = True  # sed out the graphics includes
# the introduction of edits throws off placement anyways
ldiff_flatten = True
exclude_envs = "|kleeexpr|disasm|logfile|Verbatim|FancyVerb|VerbatimEnvironment"
# --exclude-safecmd=\"kleeexpr,disasm\" --exclude-textcmd=\"kleeexpr,disasm\"
exclude_incs = "| grep -v 7Curric | grep -v Appendix- "

# for any command, return all output as an array of lines
def _cmd(cmd):
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = []
    for line in result.stdout.readlines():
        out.append(line.decode("utf-8"))
    return out


# for any command, only get the first line of output, less the \n at the end
def _cmd_l(cmd):
    return _cmd(cmd)[0][:-1]


# for any command, don't show me the output, just run it
def _cmd_p(cmd):
    print(">> " + cmd)
    return subprocess.call(cmd, shell=True)


def main(old=None, strip_figs=False):
    # find the file in the repo that is the root/main tex
    # this is the file that you would run the latex command on to compile
    mainfile = _cmd_l("git grep -l '^[ \\t]*\\\\documentclass'")
    mainbase = mainfile[:-4]
    # TODO doesn't handle multiple results,
    # just assumes first match is the correct answer
    timestamp = _cmd_l("date \"+%Y%m%d-%H:%M\"")

    # determine if this repo has changes since most recent commit
    # if it does, then compare most recent commit to current version
    # if it doesn't, then compare the 2 most recent commits
    wc_l = int(_cmd_l("git diff | wc -l"))
    # print(wc_l)

    # the the name of the most recent commit
    newest_commit = str(_cmd_l("git log --pretty=oneline --abbrev=commit -n 1")).split(" ")[0]  # noqa
    # print(newest_commit)

    new = "--"
    if old is None:
        old = newest_commit
        out = "diff-" + timestamp + "-" + old[0:7] + "-curr.pdf"
        if wc_l == 0:  # a repo without changes has 0 lines in diff
            new = newest_commit
            # the name of the second most recent commit
            old = str(_cmd_l("git log --pretty=oneline --abbrev=commit -n 2 | tail -1")).split(" ")[0]  # noqa
            out = "diff-" + timestamp + "-" + old[0:7] + "-" + new[0:7] + ".pdf"
    else:
        out = "diff-" + timestamp + "-" + old[0:7] + "-curr.pdf"

    # you can use the above as a wrapper to auto call latexdiff
    # (should it work for you)
    # to do that, use this command string:
    #     cmd = "git latexdiff --ignore-latex-errors --latexmk
    #           --output " + out + " " + old + " " + new

    # from here on, it is a port of latexdiff
    print("Main is " + mainfile)  # file you would normally use with latex
    print("New  is " + new)       # version you want to see what has changed in
    print("Old  is " + old)       # version you are basing the diff from
    print("Out  is " + out)       # name of the file this will output

    # we need to collect some environment info
    dircall = _cmd_l("pwd")
    print("Dircall " + dircall)  # this is the directory we called from
    # assumes this is the directory with the tex files
    dircall_rel = _cmd_l("git rev-parse --show-prefix")[:-1]
    # path between base of git repo and calling directory
    print("Dircall_rel " + dircall_rel)
    dirgit = _cmd_l("git rev-parse --git-dir")
    dirgit = dirgit[:-5]
    print("Dirgit " + dirgit)  # path to base of git repo

    # so now we need to make a temporary directory so we don't foo things up
    print("Creating temporary directory")
    dirtmp = "/tmp/git-latexdiff." + str(randint(1000, 9999))
    print("Dirtmp " + dirtmp)
    _cmd_p("mkdir " + dirtmp)

    # use git archive to pull a tarball of the
    # version you want into the temp dir
    print("Getting old version")
    os.chdir(dirtmp)
    _cmd("(cd " + dirgit + " && git archive --format=tar " + old + " " + dircall + ") | tar -xf -")  # noqa
    os.chdir(dircall_rel)
    print("Curr dir: " + _cmd_l("pwd"))

    # we assume that the bbls aren't tracked
    print("Making bbl for old")
    # we assume that the current bbl is good enough for
    # the old one so need to make it
    print("!! Assuming that bbl in current directory is good enough")
    _cmd_p("cp " + dircall + "/" + mainbase + ".bbl " + dirtmp + "/Paper/.")

    if ldiff_flatten:
        _cmd_p("cat \"" + mainbase + ".tex\" " + exclude_incs + "| LC_CTYPE=C sed 's/%\\\\include.*//' > \"" + mainbase + "-diffcorrected.tex\"")
        _cmd_p("cat \"" + dircall + "/" + mainbase + ".tex\" " + exclude_incs + "| LC_CTYPE=C sed 's/%\\\\include.*//' > \"" + dircall + "/" + mainbase + "-diffcorrected.tex\"")
        if _cmd_p("latexdiff --config=\"PICTUREENV=(?:picture|DIFnomarkup" + exclude_envs + ")[\\w\\d*@]*\" --flatten --ignore-warnings \"" + mainbase + "-diffcorrected.tex\" \"" + dircall + "/" + mainbase + "-diffcorrected.tex\" > diff.tex") != 0:
            print("Error, latexdiff")
            sys.exit(1)
    else:
        # converts all those many tex into a single tex, store in temp dir
        print("Latexpanding old")
        _cmd_p("latexpand \"" + mainbase + "\".tex > old-flattened.tex")

        # TODO git archive the new if new isn't '--'
        # so you can do arbitrary commit diffs
        # for now, you aren't diffing anything other than the latest two
        # if most recent commit != current, then you are doing:
        # diff     <most recent commit> <dircall>
        # if most recent commit == current, then you are doing:
        # diff <2nd most recent commit> <dircall>
        print("Latexpanding new")
        _cmd_p("(cd " + dircall + " && latexpand \"" + mainbase + "\".tex) > new-flattened.tex")  # noqa

        # this does the heavy lifting, converts two tex files
        # into a word diff that is a valid tex
        # removals are in red, additions are in blue
        print("latexdiff")
        _cmd_p("latexdiff --ignore-warnings --exclude-safecmd=kleeexpr,disasm old-flattened.tex new-flattened.tex > diff.tex")


    if repair_graphics:
        print("repair graphics")
        dirgit = dirgit.replace('/', '\\/')
        # this assumes you're me...
        # e.g. that you have all your figs not in the tex dir
        # more precisely that they are in the parent dir under Figs
        # e.g. that you have a ../Figs/<fig> convention
        # this searches for relative Figs path and
        # makes it absolute so that the tex can compile
        if strip_figs:
            _cmd_p("LC_CTYPE=C sed 's/\\includegraphics\(\[.*\]\){.*}/\\includegraphics\\1{Figplaceholder}/' diff.tex > diff2.tex")  # noqa
            _cmd_p("mv -f diff2.tex diff.tex")
        #else:
        #    _cmd_p("LC_CTYPE=C sed 's/\.\.\/Figs/" + dirgit + "\/Figs/' diff.tex > \"" + mainfile + "\"")  # noqa
        # the above combines the 'mv' that you see in the else below
    _cmd_p("mv -f diff.tex \"" + mainfile + "\"")
    print("Done making diff")

    # so now that you have a cool diff'ed tex you need to compile it
    # tex can be funny and it's best to compile, bibtex, compile
    pdffile = "%s.pdf" % mainbase
    print(latex + " 1")
    _cmd_p(latex + " \"" + mainbase + "\"")
    if not os.path.isfile(pdffile):
        print("Error, can't find %s, temp dir is %s" % (pdffile, dirtmp))
        sys.exit(1)
    print("bibtex")
    _cmd_p("bibtex " + " \"" + mainbase + "\"")
    print(latex + " 2")
    _cmd_p(latex + " \"" + mainbase + "\"")
    if not os.path.isfile(pdffile):
        print("Error, can't find %s, temp dir is %s" % (pdffile, dirtmp))
        sys.exit(1)
    # might as well compile again!
    print(latex + " 3")
    _cmd_p(latex + " \"" + mainbase + "\"")
    if not os.path.isfile(pdffile):
        print("Error, can't find %s, temp dir is %s" % (pdffile, dirtmp))
        sys.exit(1)
    # now copy the result from the temporary directory to
    # the directory you called this script from
    print("publishing")
    pdfout = dircall + "/" + out
    _cmd_p("cp \"" + mainbase + "\".pdf " + pdfout)
    print("Done pdfing")

    print("")
    # I use skim, here is a copy and paste to launch
    # skim on that new pdf you just made
    print("/Applications/Skim.app/Contents/MacOS/Skim " + pdfout)


if __name__ == "__main__":
    old = None
    if len(sys.argv) > 1:
        old = sys.argv[1]
    main(old, strip_figs=False)

