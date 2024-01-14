#!/bin/bash
#
# Determines (prints to std out) revision of the local repository copy.
#
# @author Zhenya Nyden (yev@curre.net)

svn info | grep Revision | cut -d\  -f2
