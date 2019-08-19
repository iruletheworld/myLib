# -*- coding: utf-8 -*-

'''
This module is written for Python 3.
'''

__author__  = 'Dr. GAO, Siyu'
__version__ = '3.0.0'
__date__    = '2019.08.19'

import os, csv
import time
import re
import shutil
import subprocess
import tkinter as tk
import tkinter.filedialog as fileDialog
import tkinter.messagebox as msgbox
import tkinter.simpledialog
from collections import defaultdict

from functools import wraps


import fnmatch
from random import *

CONST_STR_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# =============================================================================
# <Function: file select dialogue>
# =============================================================================
def listFileDialog(bool_multi=False, str_init_dir=os.getcwd(), str_title='', list_filetypes=list(), str_defaultextension=''):
    """
    .. _listFileDialog :
    
    Prompt a file select dialog and return the selected file(s) as a list.

    Allow single select or multi-select.

    Parameters
    ----------
    bool_multi : boolean
        The control for single select or multi-select. 
        True = multi-select
        False = single select (Default)

    str_init_dir : str
        The initial directory.
        Default is the current working directory.

    str_title : str
        The title of the dialog. 
        Default is an empty string.

    list_filetypes : list
        The file filter list. Default is an empty list.
        Consult tk's documentation for the list format.

    Returns
    -------
    list :
        If file(s) selected, than the list contains the path(s).
        Otherwise is an empty list.

        For single select, use the 1st element of the return list (its a one element list). 

    Examples
    --------
    .. code:: python

        str_paths = gsyMain.listFileDialog(bool_multi=True, str_init_dir=os.getcwd(), str_title='Choose SAV, DYR and SLD files')
    """

    try:

        root = tk.Tk()

        root.withdraw()

        if bool_multi == False:

            str_path = fileDialog.askopenfilename(parent=root, title=str_title, initialdir=str_init_dir, filetypes=list_filetypes,
                                                  defaultextension=str_defaultextension)

            str_path = str_path.split('|')

        else:

            str_path = fileDialog.askopenfilenames(parent=root, title=str_title, initialdir=str_init_dir, filetypes=list_filetypes,
                                                   defaultextension=str_defaultextension)

            str_path = list(root.tk.splitlist(str_path))

        root.destroy()

        return str_path

    except:

        # prompt fail msg
        root = tk.Tk()

        root.withdraw()

        msgbox.showinfo('Error on file selection.')

        root.destroy()

        return list()
# =============================================================================
# </Function: file select dialogue>
# =============================================================================



# =============================================================================
# <Function: a dialogue wrapper for objects>
# =============================================================================
def strDlgs(obj, str_attr_name, list_filter, str_dlg_title, 
            str_case='open', bool_multi_select=False, str_delimiter='|'):
    '''
    .. _strDlgs :

    This function is a wrapper for the dialogue funcs for objects (may update it
    using decorator in the future).

    The value of the given attribute must exists and it should be string.

    'open'
    'save'
    'dir'

    
    Prompt a file select dialog and return the selected file(s) as a list.

    Allow single select or multi-select.

    Parameters
    ----------
    str_attr_name : 

    list_filter : 

    str_dlg_title : 

    str_case : 

    bool_multi_select :

    str_delimiter :

    Returns
    -------
    list :
        If file(s) selected, than the list contains the path(s).
        Otherwise is an empty list.

        For single select, use the 1st element of the return list (its a one element list). 

    Examples
    --------
    .. code:: python

        str_paths = gsyMain.listFileDialog(bool_multi=True, str_init_dir=os.getcwd(), str_title='Choose SAV, DYR and SLD files')
    '''

    # get the attribute
    attr = getattr(obj, str_attr_name)

    str_temp = attr.GetValue()

    # if not null string, get parent dir path
    if str_temp:

        str_temp = strGetParPath(str_temp)

    else:

        str_temp = os.getcwd()

    # file select dialog
    if str_case == 'open':

        # function call
        list_path = listFileDialog( 
                                    bool_multi=bool_multi_select,
                                    str_init_dir=str_temp,
                                    str_title=str_dlg_title,
                                    list_filetypes=list_filter,
                                    str_defaultextension=''
                                    )

        # if not multi select and not null string
        if (bool_multi_select == False) and (list_path[0]):

            attr.SetValue(list_path[0])

        elif (bool_multi_select == True) and (list_path):
            
            # create a string with delimiter between each element
            attr.SetValue((' ' + str_delimiter + ' ').join(list_path))

        else:

            pass

    # file save dialog
    elif str_case == 'save':

        str_path = strSaveAsDialog(
                                    str_title=str_dlg_title,
                                    str_init_dir=str_temp,
                                    str_ext=list_filter[0][1],
                                    list_filetypes=list_filter
                                    )

        if str_path:

            attr.SetValue(str_path)

        else:

            pass

    elif str_case == 'dir':

        str_path = strDirDialog(str_title=str_dlg_title, str_init_dir=str_temp, bool_mustexist=False)

        if str_path:

            attr.SetValue(str_path)

        else:

            pass

    else:

        attr.SetValue('')
# =============================================================================
# </Function: a dialogue wrapper for objects>
# =============================================================================



# =============================================================================
# <Function: directory select dialogue>
# =============================================================================
def strDirDialog(str_title='', str_init_dir=os.getcwd(), bool_mustexist=True):
    """
    .. _strDirDialog :
    
    Prompt a diretory (folder) select dialog and return the selected directory as a string.

    Only allow single directory select.

    Parameters
    ----------
    str_title : str
        The title of the window.

    str_init_dir : str
        The initial directory.
        Default is the current working directory.

    bool_mustexist : boolean
        The directory must exist for selection.

        Default = True

    Returns
    -------
    str_path : str
        The path of the selected directory (folder). If cancel, it is an empty string.

    Examples
    --------
    .. code:: python

        from GSY import gsyMain

        str_path_export = gsyMain.strDirDialog(str_title='Select an export folder')
    """

    try:

        root = tk.Tk()

        root.withdraw()

        str_path = fileDialog.askdirectory(parent=root, title=str_title, initialdir=str_init_dir, mustexist=bool_mustexist)

        return str_path

    except:

        # prompt fail msg
        root = tk.Tk()

        root.withdraw()

        msgbox.showinfo('Error on directory selection.')

        root.destroy()

        return ''
# =============================================================================
# </Function: directory select dialogue>
# =============================================================================



# =============================================================================
# <Function: file save dialogue>
# =============================================================================
def strSaveAsDialog(str_title='', str_init_dir=os.getcwd(), str_ext='', list_filetypes=list()):
    """
    .. _strSaveAsDialog :
    
    Prompt a file save dialog.

    The path of the file will be returned.

    Parameters
    ----------
    str_title : str
        The title of the window.

    str_init_dir : str
        The initial directory.
        Default is the current working directory.

    str_ext : str
        The default extension for the file save as.
        Default = empty string

    list_filetypes : list
        File filter.

    Returns
    -------
    str_path : str
        The path of the file save as.

    Examples
    --------
    .. code:: python

        from GSY import gsyMain

        # file filter for the dialog
        list_filter = [('Excel workbook', '.xlsx')]

        # function call to get path
        str_path_xlsx = gsyMain.strSaveAsDialog(str_title='XLSX save as', list_filetypes=list_filter, str_ext='.xlsx')
    """

    try:

        root = tk.Tk()

        root.withdraw()

        str_path = fileDialog.asksaveasfilename(parent=root, title=str_title, initialdir=str_init_dir,
                                                defaultextension=str_ext, filetypes=list_filetypes)

        return str_path

    except:

        # prompt fail msg
        root = tk.Tk()

        root.withdraw()

        msgbox.showinfo('Error on file Save As selection.')

        root.destroy()

        return ''
# =============================================================================
# </Function: file save dialogue>
# =============================================================================



# =============================================================================
# <Function: file exists>
# =============================================================================
def boolPathExists(str_path, bool_dir=False):
    """
    .. _boolPathExists :
    
    Check whether the path exists or not. Can check both file's and dir's.

    If exists, return True; else, return False.

    Parameters
    ----------
    str_path : str
        The path to check.

    bool_dir : boolean
        Is the path a dir?
        True = it's a dir
        False = it is not a dir

        Default = False

    Returns
    -------
    bool_exists : boolean
        True = path exists
        False = path not found
    """

    if bool_dir == False:

        bool_exists = os.path.isfile(str_path)

    else:

        bool_exists = os.path.isdir(str_path)

    return bool_exists
# =============================================================================
# </Function: file exists>
# =============================================================================



# =============================================================================
# <Function: dynamically add path to a given environmental variable>
# =============================================================================
def boolAddPath(str_var, str_environ='PATH'):
    '''
    .. _boolAddPath :

    Dynamically add value to the environmental variable.

    If the environmental variable already exists, the value will be add to the variable.

    If the environmental variable cannot be found, it will be created and its value set to the 
    given value.

    Once exited, the added value will disappear. 

    Parameters
    ----------
    str_var : str
        The value for adding.

    str_environ : str
        The environmental value to add to. The default is the 'PATH' environmental variable.

    Returns
    -------
    boolean:
        Returns True if no exception. Return False on exception.

    Reference
    -------
    https://stackoverflow.com/questions/44505457/checking-if-an-environment-variable-exists-and-is-set-to-true?rq=1
    '''

    str_temp = os.environ.get(str_environ)

    # debug use
    # print(str_temp)

    str_msg_empty_str = 'The value of the environmental variable to be added cannot be an empty string.'

    str_msg_environ_not_found = 'Environmental variable not found. Try to add it.'

    str_msg_environ_found = 'Environmental variable found. Try to add the value to it.'

    try:

        if not str_var:

            raise IOError(str_msg_empty_str)

        else:

            pass
        
        if not str_temp:

            print(str_msg_environ_not_found)

            os.environ[str(str_environ)] = str(str_var)

        else:

            print(str_msg_environ_found)

            os.environ[str(str_environ)] = os.environ[str(str_environ)] + ';' + str(str_var)

        return True

    except:

        return False
# =============================================================================
# </Function: dynamically add path to a given environmental variable>
# =============================================================================



# =============================================================================
# <Function: prompt a message box>
# =============================================================================
def promptMsg(str_title='', str_msg='', str_type='info'):
    """
    .. _promptMsg :     
        
    This function is a wrapper for tk's three different message boxes.
        
    This function prompts a message box with the message given.
    
    Parameters
    ----------
    str_title : str
        Title of the message box.

    str_msg : str
        The message to be shown.

    str_type : str, default = "info"
        Type of the message box.

        * "info" = information message box. This is the default value.
        * "err" = error message box
        * "warn" = warning message box


    Returns
    -------    
    None
    
    Examples
    --------
    .. code:: python
    
        import tkinter as tk
        import tkinter.messagebox as msgbox

        import gsyIO

        gsyMain.promptMsg('message title', 'message body', 'err')
    """
    # make tk main window-----------------------------------------------------#
    root = tk.Tk()

    # hide tk main window-----------------------------------------------------#
    root.withdraw()

    # prompt info msg---------------------------------------------------------#
    if str_type == 'info':

        msgbox.showinfo(str_title, str_msg)

    # prompt error msg--------------------------------------------------------#
    elif str_type == 'err':

        msgbox.showerror(str_title, str_msg)

    # prompt warning msg------------------------------------------------------#
    elif str_type == 'warn':

        msgbox.showwarning(str_title, str_msg)

    # default, prompt info msg------------------------------------------------#
    else:
        
        msgbox.showinfo(str_title, str_msg)

    # destroy tk main window--------------------------------------------------#
    root.destroy()
# =============================================================================
# </Function: prompt a message box>
# =============================================================================



# =============================================================================
# <Function: get system time and date>
# =============================================================================
def dateTimeNow(str_sign=''):
    """
    .. _dateTimeNow :
    
    Return the system date and time as a string.

    Return format: 'yyyy-mm-dd, HH:MM:SS' + str_sign

    Parameters
    ----------
    str_sign : str
        A sign to append to the 'yyyy-mm-dd, HH:MM:SS'.

    Returns
    -------
    str_date_time : str
        Formatted system date time string in 'yyyy-mm-dd, HH:MM:SS' + str_sign.         

    Examples
    --------
    >>> dateTimeNow(':')
    '2017-11-20, 15:14:42:'
    """

    str_date_time = time.strftime('%Y-%m-%d, %H:%M:%S', time.gmtime())

    str_date_time = str_date_time + str_sign

    return str_date_time
# =============================================================================
# </Function: get system time and date>
# =============================================================================



# =============================================================================
# <Function: get filename from path>
# =============================================================================
def strGetFilename(str_path, bool_with_ext=False):
    """
    .. _strGetFilename :
    
    Get the filename from a path. With or without the extension.

    Parameters
    ----------
    str_path : str
        The path of the file.

    bool_with_ext : boolean
        Whether to include the extension.

        True = include the extension
        False = not include the extension

        Default = False

    Returns
    -------
    str_filename : str
        The filename from the path.

    Examples
    --------
    .. code:: python

        >>> str_path_file = 'c:/some.txt'
        >>> strGetFilename(str_path_file)
        'some'
        >>> strGetFilename(str_path_file, True)
        'some.txt'
        >>>
    """

    str_filename = ''

    if bool_with_ext:

        str_filename = os.path.basename(str_path)

    else:

        str_filename = os.path.basename(str_path)

        str_filename = os.path.splitext(str_filename)[0]

    return str_filename
# =============================================================================
# </Function: get filename from path>
# =============================================================================



# =============================================================================
# <Function: strip the file's path of its extension>
# =============================================================================
def strStripExt(str_path_file):
    '''
    .. _strStripExt :
    
    This function removes the given file path's extension and returns the path.

    Parameters
    ----------
    str_path_file : str
        The file path.

    Returns
    -------
    str_temp : str
        The file path with the file extension stripped.

    Examples
    --------
    .. code:: python

        >>> str_path_file = 'c:/some.txt'
        >>> strStripExt(str_path_file)
        'c:/some'
        >>> str_path_file = 'c:/some'
        >>> strStripExt(str_path_file)
        'c:/some'
        >>>
    '''

    str_temp = ''

    str_temp = os.path.splitext(str_path_file)[0]

    return str_temp
# =============================================================================
# </Function: strip the file's path of its extension>
# =============================================================================



# =============================================================================
# <Function: delete file>
# =============================================================================
def deleteFile(str_filepath, bool_verbose=False):
    """
    .. _deleteFile :
    
    Delete a file from the given path. Needs the "os" module.

    Parameters
    ----------
    str_filepath : str
        The path of the file.

    Returns
    -------
    boolean :
        Returns True if no exception. Returns False on exception.

    Examples
    --------
    .. code:: python

        import gsyMain

        str_path = r'c:/folder/file.file'

        bool_temp = gsyMain.deleteFile(str_path)
    """

    try:

        if os.path.isfile(str_filepath):

            os.unlink(str_filepath)

            if bool_verbose:

                print(('File deleted : ' + str_filepath))

            else:

                pass

            return True

        else:

            return False

    except Exception as e:

        print(e)

        return False
# =============================================================================
# </Function: delete file>
# =============================================================================



# =============================================================================
# <Function: delete folder>
# =============================================================================
def deleteDir(str_dir_path, bool_verbose=False):
    """
    .. _deleteDir :
    
    Delete a directory from the given path. Needs the "os" module and the "shutil" module.

    Parameters
    ----------
    str_dir_path : str
        The path of the directory.

    Returns
    -------
    boolean :
        Returns True if no exception. Returns False on exception.

    Examples
    --------
    .. code:: python

        import gsyMain

        str_path = r'c:/folder'

        bool_temp = gsyMain.deleteDir(str_path)
    """

    try:

        if os.path.isdir(str_dir_path):

            shutil.rmtree(str_dir_path)

            if bool_verbose:

                print(('Direcotry deleted : ' + str_dir_path))

            else:

                pass

            return True

        else:

            return False

    except Exception as e:

        print(e)

        return False
# =============================================================================
# </Function: delete folder>
# =============================================================================



# =============================================================================
# <Function: delete all>
# =============================================================================
def deleteAll(str_dir_path, bool_also_dir=False):
    """
    .. _deleteDir :
    
    Delete all files under a directory. Optionally delete all subdirectories and their files.

    Parameters
    ----------
    str_dir_path : str
        The path of the directory.

    bool_also_dir : boolean
        Whether to delete all subdirectories and their files.

        True = delete
        False = not delete

        Default = False

    Returns
    -------
    boolean :
        Returns True if no exception. Returns False on exception.

    Examples
    --------
    .. code:: python

        import gsyMain

        str_path = r'c:/folder'

        bool_temp = gsyMain.deleteDir(str_path, True)
    """

    try:

        for i in os.listdir(str_dir_path):

            str_temp = os.path.join(str_dir_path, i)

            if os.path.isfile(str_temp):

                    deleteFile(str_temp)

            else:

                pass

            if bool_also_dir:

                if os.path.isdir(str_temp):

                    deleteDir(str_temp)

            else:

               pass

        return True

    except Exception as e:
        
        print(e)

        return False
# =============================================================================
# </Function: delete all>
# =============================================================================



# =============================================================================
# <Function: get all file paths with filter>
# =============================================================================
def listGetPathRecursive(str_scr, str_filter):
    '''
    .. _listGetPathRecursive :
    
    This function walks every sub dir inside the given source dir and returns the 
    files' paths that matches the file filter.

    Parameters
    ----------
    str_scr : str
        The given source dir.

    str_filter : str
        The file filter. Need to be in the format of '*.filter'.

    Returns
    -------
    list_paths : list
        The list containing all the file paths found. Or
        and empty list.

    Example
    -------
    .. code:: python

        >>> str_dir = '.../Global variables'
        >>> listGetPathRecursive(str_dir, '*.txt')
        ['.../Global variables\\Strong\\Strong_A_for_PSCAD.txt', '.../Global variables\\Strong\\Strong_B_for_PSCAD.txt']
        >>> listGetPathRecursive(str_dir, '*.add')
        []
        >>> listGetPathRecursive(str_dir, 'txt')
        []
        >>>
    '''


    bool_temp = boolPathExists(str_scr, bool_dir=True)

    if bool_temp:

        list_paths = []

        for root, dirnames, filenames in os.walk(str_scr):

            for filename in fnmatch.filter(filenames, str_filter):

                list_paths.append(os.path.join(root, filename))

        return list_paths

    else:

        print('Source directory not found.')

        return list()
# =============================================================================
# </Function: get all file paths with filter>
# =============================================================================



# =============================================================================
# <Function: get parent path>
# =============================================================================
def strGetParPath(str_scr):
    '''
    .. _strGetParPath :
    
    This function returns the parent path of the given path.

    Parameters
    ----------
    str_scr : str
        The given path.

    Returns
    -------
    str_temp : str
        The parent path of the given path.

    Reference
    ---------
    https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number

    Example
    -------
    .. code:: python

        >>> str_par = os.path.join('c:/', 'parent', 'scr')
        >>> str_par
        'c:/parent\\scr'
        >>> strGetParPath(str_par)
        'c:\\parent'
        >>>
    '''

    str_temp = os.path.abspath(os.path.join(str_scr, os.pardir))

    return str_temp
# =============================================================================
# </Function: get parent path>
# =============================================================================



# =============================================================================
# <Function: convert a string of numbers to a list>
# =============================================================================
def listNumStr2List(str_in, str_delimit=',', str_type='int'):
    '''
    .. _listNumStr2List :
    
    This function converts a delimited, numericable string into a list.

    Supports all int or all float.

    Parameters
    ----------
    str_in : str
        The input string.

    str_delimit : str
        The delimiter. Default = ','

    str_type : str
        Specify the number type. Default = 'int'

        If not default, this function would try to convert the string to float.
        
    Returns
    -------
    list_temp : list
        The converted list.

    Reference
    ---------
    https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number

    Example
    -------
    .. code:: python

        >>> a = '1, 2, 3, 4, 5,     0'
        >>> listNumStr2List(a)
        [1, 2, 3, 4, 5, 0]
        >>> a = '1.0,2.0,3.0'
        >>> listNumStr2List(a)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "...\gsyMain.py", line 819, in listNumStr2List

        ValueError: invalid literal for int() with base 10: '1.0'
        >>> listNumStr2List(a, str_type='float')
        [1.0, 2.0, 3.0]
        >>> b = '1|2|3'
        >>> listNumStr2List(b, '|')
        [1, 2, 3]
        >>>
    '''

    list_temp = []

    if str_type == 'int':

        list_temp = list(map(int, str_in.split(str_delimit)))

    else:

        list_temp = list(map(float, str_in.split(str_delimit)))

    return list_temp
# =============================================================================
# </Function: convert a string of numbers to a list>
# =============================================================================



# =============================================================================
# <Function: increase the given char by 1>
# =============================================================================
def strAdd1(str_in):
    '''
    .. _strAdd1 :
    
    This function increase the given character by one and returns the next character.

    Parameters
    ----------
    str_in : str
        The input character. Only 1 character. Do not input strings.
        
    Returns
    -------
    str_temp : str
        The character follows the given character.

    Reference
    ---------
    https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number

    Example
    -------
    .. code:: python

        >>> in_1 = 'a'
        >>> strAdd1(in_1)
        'b'
        >>> in_2 = 'z'
        >>> strAdd1(in_2)
        '{'
        >>> in_3 = 'Z'
        >>> strAdd1(in_3)
        '['
        >>> in_4 = 'X'
        >>> strAdd1(in_4)
        'Y'
        >>>
    '''

    str_temp = str_in

    str_temp = chr(ord(str_temp) + 1)

    return str_temp
# =============================================================================
# </Function: increase the given char by 1>
# =============================================================================



# =============================================================================
# <Function: decrease the given char by 1>
# =============================================================================
def strMinus1(str_in):
    '''
    
    '''

    str_temp = str_in

    str_temp = chr(ord(str_temp) - 1)

    return str_temp
# =============================================================================
# </Function: decrease the given char by 1>
# =============================================================================



# =============================================================================
# <Function: create Excel column address (string) from column index (int)>
# =============================================================================
def strExcelColAddr(int_col):
    '''
    1 based index
    '''

    str_col = []

    int_rem = 0

    while int_col:

        int_col, int_rem = divmod(int_col - 1, 26)

        str_col[:0] = CONST_STR_LETTERS[int_rem]

    str_temp = ''.join(str_col)

    return str_temp
# =============================================================================
# </Function: create Excel column address (string) from column index (int)>
# =============================================================================


# =============================================================================
# <Function: create Excel cell address>
# =============================================================================
def strExcelAddr(int_row, int_col):
    """
    .. _strExcelAddr :
    
    This function converts given row number and column number to an Excel-style cell name.

    Parameters
    ----------
    *dicts : multiple given dictionaries.
        
    Returns
    -------
    int_row : int
        The row number.

    int_col : int
        The column number.

    Reference
    ---------
    https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number

    Example
    -------
    .. code:: python

        >>> int_row = 2
        >>> int_col = 10
        >>> strExcelAddr(int_row, int_col)
        'J2'
        >>> int_row = 1
        >>> int_col = 1
        >>> strExcelAddr(int_row, int_col)
        'A1'
        >>> 
    """
    
    # LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # result = []

    # while int_col:

    #     int_col, rem = divmod(int_col - 1, 26)

    #     result[:0] = CONST_STR_LETTERS[rem]

    str_col = strExcelColAddr(int_col)

    # return ''.join(result) + str(int_row)

    return str_col + str(int_row)
# =============================================================================
# </Function: create Excel cell address>
# =============================================================================



# =============================================================================
# <Function: calculate Excel column index>
# =============================================================================
def intExcelColIndex(str_Col, int_limit=16384):
    '''
    '''

    str_Col = str_Col.upper()

    # reverse the input string for easier manipulation
    str_Col = str_Col[::-1]

    int_len = len(str_Col)

    i = 0

    int_index = 0

    for i in range(0, int_len):

        str_temp = str_Col[i]

        if str_temp in CONST_STR_LETTERS:

            pass

        else:

            str_msg = 'Input column address contains non alphabetical letter.'

            raise ValueError(str_msg)

        int_pos = CONST_STR_LETTERS.index(str_temp)

        int_pos = int_pos + 1

        int_index = int_index + int_pos * (26**i)

    if int_index <= int_limit:

        return int_index

    else:

        str_Col = str_Col[::-1]

        str_msg = ('The input column address '
                    +'"'
                    + str_Col
                    + ' ('
                    + str(int_index)
                    + ') '
                    + '"' +
                    ' is larger than the limit '
                    + str(int_limit))

        raise ValueError(str_msg)
# =============================================================================
# </Function: calculate Excel column index>
# =============================================================================



# =============================================================================
# <Function: merge dictionaries>
# =============================================================================
def dictMerge(*dicts):
    '''
    .. _dictMerge :
    
    This function mergers given dictionaries.

    Parameters
    ----------
    *dicts : multiple given dictionaries.
        
    Returns
    -------
    dict_temp : dictionary
        The merged dictionary.

    Example
    -------
    .. code:: python

        >>> aa = {'a':1, 'b':2}
        >>> cc = {'c':3, 'd':4}
        >>> dictMerge(aa, cc)
        {'a': 1, 'c': 3, 'b': 2, 'd': 4}
        >>> dictMerge(aa)
        {'a': 1, 'b': 2}
        >>> ee = {1:100, 2:200}
        >>> dictMerge(aa, cc, ee)
        {'a': 1, 1: 100, 'c': 3, 'b': 2, 'd': 4, 2: 200}
        >>>
    '''

    # initialisation
    dict_temp = {}

    # loop through all the input parameters and merge them
    for i in dicts:

        dict_temp.update(i)

    return dict_temp
# =============================================================================
# </Function: merge dictionaries>
# =============================================================================



# =============================================================================
# <Function: get an pseudo random int that is not in the list>
# =============================================================================
def intGet(list_range):
    '''
    .. _intGet :
    
    This function returns a pseudo randomly generated int that is not in the given list.

    This function would first try to get an int inside the min and max of the given list
    but not in the list. After len(list_range) attempts, the max would be doubled to allow
    a wider range for randoming.

    This function was originally written using recursion. But then I hit the limit of the 
    stack. So I changed it to use iteration, which is limited by the size of memory.

    Parameters
    ----------
    list_range : list
        A list of int. The return int will not be in this list.

    Returns
    -------
    i : int
        A pseudo randomly generated int that is not in the given list.

    Example
    -------
    .. code:: python

        >>> a = [1, 2, 3, 4, 5, 10]
        >>> intGet(a)
        7
        >>> a = [1, 2, 3]
        >>> intGet(a)
        5
        >>>
    '''

    # get min of the list
    int_min = min(list_range)

    # get max of the list
    int_max = max(list_range)

    # get random
    i = randint(int_min, int_max)

    # iteration, limited by the size of memory
    j = 0

    while i in list_range:

        i = randint(int_min, int_max)

        j = j + 1

        # this is to jump out of loop
        if j > len(list_range):

            int_max = max(list_range) * 2

    return i
# =============================================================================
# </Function: get an pseudo random int that is not in the list>
# =============================================================================



# =============================================================================
# <Function: check if a process is running>
# =============================================================================
def boolProcessExists(str_process_fullname):
    '''
    .. _boolProcessExists :
    
    This function checks whether a given process is running or not.

    Parameters
    ----------
    str_process_fullname : string
        The fullname of the process

    Returns
    -------
    bool_temp : bool
        True = process found; False = process not found

    Reference
    ---------
    # https://stackoverflow.com/questions/7787120/python-check-if-a-process-is-running-or-not

    Example
    -------
    .. code:: python

        >>> from gsyMain import *
        >>> s = 'EXCEL.EXE'
        >>> boolProcessExists(s)
        True
        >>> s = 'excel.exe'
        >>> boolProcessExists(s)
        True
        >>> s = 'nosuchprocess.exe'
        >>> boolProcessExists(s)
        False
        >>>
    '''

    call = 'TASKLIST', '/FI', 'imagename eq %s' % str_process_fullname

    # use buildin check_output right away
    output = subprocess.check_output(call)

    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]

    last_line = last_line.lower()

    bool_temp = last_line.startswith(str_process_fullname.lower())

    return bool_temp
# =============================================================================
# </Function: check if a process is running>
# =============================================================================



# =============================================================================
# <Function: get the first smallest value in a list>
# =============================================================================
def intFirstMin(list_numeric):
    '''
    .. _intLastMin :
    
    This function scans the list from the start; finds the first smallest value and then returns
    its index.

    Parameters
    ----------
    list_numeric : list
        The list to be scanned.

        Ideally a numeric list (int or float). String lists also seems to work, but you need to know
        what it means for string lists.

    Returns
    -------
    j : int
        The index of the first smallest element in the input list.

    Examples
    --------
    .. code:: python

        >>> from gsyMain import *
        >>> a = [4, 3, 2, 1, 5, 0, 6]
        >>> b = intFirstMin(a)
        >>> b
        3
        >>> a[b]
        1
        >>>
    '''

    # begin from the first element
    i = 0

    # initialisation
    j = 0

    # while loop search
    while i <= (len(list_numeric) - 2):

        # set old value as the current indexed one
        old = list_numeric[i]

        # new value as the one behind the old one
        new = list_numeric[i + 1]

        # if the new value is smaller than the old one, 
        # need to look for the next one
        if new < old:

            # since the new is smaller than the old, 
            # set the var holding the stat to the index
            # of the one before the old
            j = i + 1

            pass

        # if the new value if bigger than the old one,
        # that means the last smallest is found, break loop
        else:

            # since the old one is smaller the new one, 
            # set the state var to the old one's index
            j = i
            
            break

        # index increment
        i += 1

    # return the index found
    return j
# =============================================================================
# </Function: get the first smallest value in a list>
# =============================================================================



# =============================================================================
# <Function: get the last smallest value in a list>
# =============================================================================
def intLastMin(list_numeric):
    '''
    .. _intLastMin :
    
    This function scans the list from the end; finds the first smallest value and then returns
    its index.

    Parameters
    ----------
    list_numeric : list
        The list to be scanned.

        Ideally a numeric list (int or float). String lists also seems to work, but you need to know
        what it means for string lists.

    Returns
    -------
    j : int
        The index of the last smallest element in the input list.

    Examples
    --------
    .. code:: python

        >>> from gsyMain import *
        >>> a = [1, 2, 3, 1, 4]
        >>> b = intLastMin(a)
        >>> b
        3
        >>> a[b]
        1
        >>>
    '''

    # begin from the last element
    i = len(list_numeric) - 1

    # initialisation
    j = 0

    # while loop search
    while i >= 1:

        # set old value as the current indexed one
        old = list_numeric[i]

        # new value as the one before the old one
        new = list_numeric[i - 1]

        # if the new value is smaller than the old one, 
        # need to look for the next one
        if new < old:
            
            # since the new is smaller than the old, 
            # set the var holding the stat to the index
            # of the one before the old
            j = i - 1

            pass

        # if the new value if bigger than the old one,
        # that means the last smallest is found, break loop
        else:
            
            # since the old one is smaller the new one, 
            # set the state var to the old one's index
            j = i
            
            break

        # index decrement
        i -= 1

    # return the index found
    return j
# =============================================================================
# </Function: get the last smallest value in a list>
# =============================================================================



# =============================================================================
# <Function: convert a string to a list>
# =============================================================================
def listStr2List(str_in, str_delimiter=','):
    '''
    .. listStr2List :
    
    This function converts a string into a list.

    Parameters
    ----------
    str_in : string
        The input string to be converted.

    str_delimiter : string
        The delimiter of the string. The default is the comma.

        Default = ','

    Returns
    -------
    list_temp : list
        The list results from conversion.

    Examples
    --------
    .. code:: python

        >>> a = 'abc|xyz'
        >>> listStr2List(a, '|')
        ['abc', 'xyz']
        >>>
    '''

    list_temp = str_in.split(str_delimiter)

    return list_temp
# =============================================================================
# </Function: convert a string to a list>
# =============================================================================



# =============================================================================
# <Function: create a dir>
# =============================================================================
def boolMakeDir(str_dir):
    '''
    .. boolMakeDir :
    
    This function would attempt to create a directory.

    If the directory already exists, this function would do nothing and
    returns False.

    This function would also returns False on exception.

    Parameters
    ----------
    str_dir : string
        The directory path that this function would try to create.

    Returns
    -------
    bool_temp : bool
        True = dir not already exists and creation process has no exception.

        False = dir already exists or exception during creation.
    '''

    bool_temp = boolPathExists(str_dir, True)

    # dir already exists
    if bool_temp:

        print('The directory already exists.')

        return False

    else:

        try:

            os.makedirs(str_dir)

        except:

            print('Error during directory make.')

            return False

        return True
# =============================================================================
# </Function: create a dir>
# =============================================================================



# =============================================================================
# <Function: prompt a yes no message box>
# =============================================================================
def boolMsgYesno(str_title='', str_msg=''):
    '''
    '''

    root = tk.Tk()

    root.withdraw()

    bool_temp = False

    bool_temp = msgbox.askyesno(str_title, str_msg)

    root.destroy()

    return bool_temp
# =============================================================================
# </Function: prompt a yes no message box>
# =============================================================================



# =============================================================================
# <Function: ask user to input an int
# =============================================================================
def intAskInt(str_title='', str_lbl=''):
    '''
    '''

    root = tk.Tk()

    root.withdraw()

    int_temp = tkinter.simpledialog.askinteger(str_title, str_lbl, parent=root)

    root.destroy()

    return int_temp
# =============================================================================
# </Function: ask user to input an int
# =============================================================================


# ===========================================================================================
# <Function: decorator for saving a list (returned by the actual func) as a CSV file>
# ===========================================================================================
def savAsCsv(func):
    '''
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):

        # prompt file save as diglog
        str_title = 'Save file as'

        list_filter = [('CSV file', '.csv')]

        str_path_suffix = strSaveAsDialog(str_title=str_title,
                                          str_init_dir=os.getcwd(),
                                          str_ext='',
                                          list_filetypes=list_filter)

        if str_path_suffix:

            list_temp = func(*args, **kwargs)

            # write to CSV file
            with open(str_path_suffix, 'w') as fout:

                for i in list_temp:

                    fout.write(','.join(i))
                    fout.write('\n')

            str_msg = 'Suffix file exported : ' + str_path_suffix

            print(str_msg)

            return str_msg

        else:

            pass

    return wrapper
# ===========================================================================================
# </Function: decorator for saving a list (returned by the actual func) as a CSV file>
# ===========================================================================================



# ===========================================================================================
# <Function: to get the length of an integer>
# ===========================================================================================
def intLenInt(int_input):
    '''
    https://stackoverflow.com/questions/2189800/length-of-an-integer-in-python
    '''

    import math

    if int_input < 0:

        int_input = -1 * int_input

    else:

        pass

    if (int_input > 0) and (int_input <= 999999999999997):

        int_length = int(math.log10(int_input)) + 1

    elif int_input > 999999999999997:

        int_length = 15

        while int_input >= 10**int_length:

            int_length += 1

    elif int_input == 0:

        int_length = 1

    else:

        raise ValueError('Value Error')

        # int_length = int(math.log10(-int_input)) + 1 # +1 if you don't count the '-' 

    return int_length
# ===========================================================================================
# </Function: to get the length of an integer>
# ===========================================================================================



# ===========================================================================================
# <Function: get CSV header>
# ===========================================================================================
def listGetCsvHeader(str_path, str_delimiter=','):
    '''
    '''

    list_header = []

    # get header
    with open(str_path, 'r') as fin:

        list_header = next(csv.reader(fin, delimiter=str_delimiter))

    return list_header
# ===========================================================================================
# </Function: get CSV header>
# ===========================================================================================



# ===========================================================================================
# <Function: get CSV column data by column index>
# ===========================================================================================
def listGetCsvCol(str_path, int_indexCol, str_delimiter=','):
    '''
    .. _listGetCsvCol :
    
    This function gets the column data in the given CSV file by column index.

    Parameters
    ----------
    str_path : str
        The full file path of the CSV file.

    int_indexCol : int
        The column index (0 based).

    Returns
    -------
    list_data : list
        The column data.

    Reference
    ----------
    https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-csv-file-with-csv-module
    '''

    cols = defaultdict(list)

    list_header = []

    # get header
    with open(str_path, 'r') as fin:

        list_header = next(csv.reader(fin, delimiter=str_delimiter))

    with open(str_path, 'r') as fin:

        reader = csv.DictReader(fin, delimiter=str_delimiter)

        for row in reader:

            for (k, v) in list(row.items()):

                cols[k].append(v)

    list_data = cols[list_header[int_indexCol]]

    return list_data
# ===========================================================================================
# </Function: get CSV column data by column index>
# ===========================================================================================



# ===========================================================================================
# <Function: start a file with system default application>
# ===========================================================================================
def start(str_path):
    '''
    .. start :
    
    This function starts a file using the system default application.

    Parameters
    ----------
    str_path : str
        The full file path of the file.

    Returns
    -------
    None.
    '''

    os.startfile(str_path)
# ===========================================================================================
# </Function: start a file with system default application>
# ===========================================================================================


# ===========================================================================================
# <Function: concat CSV files using shutil>
# ===========================================================================================
def csvConcat(list_csv_file, str_path_out):
    '''
    .. _csvConcat :
    
    This function concats CSV files using shutil.

    All CSV files are assumed to have the same header and data format.

    Only the header of the first file will be kept. The actual data will be concated. 

    Parameters
    ----------
    list_csv_file : list
        A str list of all the full paths of the CSV files.

    str_path_out : str
        Full file path for the output CSV file (concated).

    Raises
    ----------
    IO Error :
        When operation fails.

    Returns
    -------
    None.

    Reference
    ----------------------
    https://stackoverflow.com/questions/2512386/how-to-merge-200-csv-files-in-python
    https://stackoverflow.com/questions/44791212/concatenating-multiple-csv-files-into-a-single-csv-with-the-same-header-python/44791368
    '''

    try:

        # use the shell utility to concate
        with open(str_path_out, 'wb') as fout:

            for i, fname in enumerate(list_csv_file):

                # Throw away header on all but first file
                with open(fname, 'rb') as infile:

                    if i != 0:

                        infile.readline()

                    # Block copy rest of file from input to output without parsing
                    shutil.copyfileobj(infile, fout)

        return True

    except:

        raise IOError('Failed to concat CSV files.')
# ===========================================================================================
# </Function: concat CSV files using shutil>
# ===========================================================================================



# ===========================================================================================
# <Function: convert two lists into a dict>
# ===========================================================================================
def dict2Lists(list_key, list_val):
    '''
    .. _dict2Lists :
    
    This function converts two lists into one dictionary. Note that if the two lists do not have 
    the same length, funny things may happen.

    Parameters
    ----------
    list_key : list
        The lists stores all the keys.

    list_val : list
        The lists stores all the values.

    Returns
    -------
    dict_temp : dict
        The converted dictionary.

    Reference
    ----------------------
    https://stackoverflow.com/questions/209840/convert-two-lists-into-a-dictionary
    '''

    dict_temp = dict(list(zip(list_key, list_val)))

    return dict_temp
# ===========================================================================================
# </Function: convert two lists into a dict>
# ===========================================================================================



# ===========================================================================================
# <Function: search and replace in a txt like file>
# ===========================================================================================
def boolFileReplace(dict_term, str_path_in, str_path_out):
    '''
    .. _boolFileReplace :
    
    This function opens a given txt like file, use the given dictionary to search and replace, 
    then output the results to a new file.

    Note that you need to make sure that the keys and values of the dict_term are both strings. 
    Otherwise, your out file may be empty.

    Parameters
    ----------
    dict_term : dict
        The dictionary that contains the search/replacement pairs.

    str_path_in : str
        Full file path of the input file.

    str_path_out : str
        Full file path of the output file.

    Returns
    -------
    bool : bool
        True = no exception; False = on exception

    Reference
    ----------------------
    https://stackoverflow.com/questions/13089234/replacing-text-in-a-file-with-python
    '''

    try:

        with open(str_path_in, 'r') as fin, open(str_path_out, 'w+') as fout:

            for line in fin:

                for src, target in dict_term.items():

                    if src in line:

                        line = line.replace(src, target)

                    else:

                        pass

                fout.write(line)

        return True

    except:

        return False
# ===========================================================================================
#/ <Function: search and replace in a txt like file>
# ===========================================================================================



# =============================================================================
# <Function: get system local time and date>
# =============================================================================
def strLocalTime(str_format):
    """
    .. _strLocalTime :
    
    Return the system local date and time as a string according to the given format.

    Parameters
    ----------
    str_format : str
        Date/Time code format.

        Example: '%Y-%m-%d, %H:%M:%S'


    Returns
    -------
    str_date_time : str
        Formatted system local date time string.
    """

    str_date_time = time.strftime(str_format, time.localtime())

    return str_date_time
# =============================================================================
# </Function: get system local time and date>
# =============================================================================



# =============================================================================
# <Function: find all the positions of a substring in a string>
# =============================================================================
def listPosInStr(str_in, str_sub):
    '''
    .. _listPosInStr :
    
    This function finds the positions of the str_sub in the str_in and returns them as a list.

    Parameters
    ----------
    str_in : str
        The original string for searching.

    str_sub : str
        The substring to be searched.

    Returns
    -------
    list_temp : list
        The list that contains the positions of the str_sub

    Reference
    ----------------------
    https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python/32794963#32794963
    '''

    list_temp = [pos for pos, char in enumerate(str_in) if char == str_sub]

    return list_temp
# =============================================================================
# </Function: find all the positions of a substring in a string>
# =============================================================================



# =============================================================================
# <Function: natural sort>
# =============================================================================
def listNaturalSort(l): 
    '''
    https://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
    '''
    convert = lambda text: int(text) if text.isdigit() else text.lower() 

    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 

    return sorted(l, key = alphanum_key)
# =============================================================================
# </Function: natural sort>
# =============================================================================



# =============================================================================
# <Function: remove duplicates from a list>
# =============================================================================
def listRmDupe(list_in):
    '''
    https://www.w3schools.com/python/python_howto_remove_duplicates.asp
    '''

    list_out = list(dict.fromkeys(list_in))

    return list_out
# =============================================================================
# </Function: remove duplicates from a list>
# =============================================================================



# =============================================================================
# <Function: check if all elements are unique in a 1-D list>
# =============================================================================
def boolAllUnique(list_in):
    '''
    https://stackoverflow.com/questions/5278122/checking-if-all-elements-in-a-list-are-unique
    '''

    seen = set()

    return not any(i in seen or seen.add(i) for i in list_in)
# =============================================================================
# <Function: check if all elements are unique in a 1-D list>
# =============================================================================



# =============================================================================
# <Function: Get the duplicated elements and their indexes>
# =============================================================================
def genDupe(seq):
    '''
    https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
    '''

    tally = defaultdict(list)

    for i,item in enumerate(seq):

        tally[item].append(i)
        
    return ((key,locs) for key,locs in list(tally.items()) if len(locs)>1)
# =============================================================================
# </Function: Get the duplicated elements and their indexes>
# =============================================================================



# =============================================================================
# <Function: Check if two lists have any shared element>
# =============================================================================
def boolHaveShare(list_a, list_b):
    '''
    https://stackoverflow.com/questions/3170055/test-if-lists-share-any-items-in-python
    '''

    return not set(list_a).isdisjoint(list_b)
# =============================================================================
# </Function: Check if two lists have any shared element>
# =============================================================================



def saveAsTxt(str_txt='', str_path_txt=''):
    '''
    '''

    with open(str_path_txt, 'w+') as fout:

        fout.write(str_txt)




# =============================================================================
# <Function: To diff two CSVs>
# =============================================================================
def diffCsv(str_path_csv1, str_path_csv2, str_path_out='', str_delimiter=',', 
            int_delimiter_index=2,
            str_status_added='Added',str_status_rmed='Removed',str_status_chnged='Changed',
            bool_sort=True):
    '''
    .. _diffCsv :
    
    This function performs diffing of two CSV files.

    The base file is the first input file. The status are 'Added', 'Changed' and 'Removed'.

    If an valid output file path is provided the data will be write to the file. 
    Otherwise, the data will be returned as a tuple.

    Parameters
    ----------
    str_path_csv1 : str
        Full file path of the first input CSV file. This file is used as the base file.

    str_path_csv2 : str
        Full file path of the second input CSV file.

    str_path_out : str
        The full file path for the output CSV file.

        Optional. Default is an empty string.
        
    str_delimiter : str
        The delimiter for the two input CSV files.

    int_delimiter_index : int
        Zero based index of the delimiter for forming search keys.

        This function uses the string up to and include the indexed delimiter to form the search keys
        to calculate the status.

        Example:

            if int_delimiter_indexint_delimiter_index = 2, then the search keys will be formed by the 
            the values of the first 3 cols and the 3 delimiters.

    str_status_added : str
        The status string for status 'Added'.

        Default = 'Added'

    str_status_rmed : str
        The status string for status 'Removed'

        Default = 'Removed'

    str_status_chnged : str
        The status string for status 'Changed'

        Default = 'Changed'

    bool_sort : bool
        Whether to sort the outputs. This function would attempt to use natural sort.

        Default = True

    Returns
    -------
    None : If the input argument str_path_out is valid. The data will be written to the file.

    A tuple of 3 lists for different status : in the order of 'Added', 'Changed' and 'Removed'
        (list_added_to_data1, list_changed_in_data1, list_removed_from_data1)
    '''

    list_header = listGetCsvHeader(str_path_csv1, str_delimiter=str_delimiter)

    list_data1 = []
    list_data2 = []

    with open(str_path_csv1, 'r') as fin1, open(str_path_csv2, 'r') as fin2:

        list_data1 = list(fin1)

        list_data2 = list(fin2)

    set_data1 = set(list_data1)
    set_data2 = set(list_data2)

    set_removed_from_data1 = set_data1 - set_data2
    set_added_to_data1     = set_data2 - set_data1

    list_removed_from_data1 = list(set_removed_from_data1)
    list_added_to_data1     = list(set_added_to_data1)

    # form search keys
    list_key = []

    for i in range(0, len(list_removed_from_data1)):

        str_temp = list_removed_from_data1[i]

        # find the positions of the delimiter
        list_pos = [j.start() for j in re.finditer(str_delimiter, str_temp)]

        str_temp = str_temp[:list_pos[int_delimiter_index]+1]

        list_key.append(str_temp)


    # search for the changed in the added to data1
    # store the indices
    list_index_changed_in_added_to = []

    for i in list_key:

        for k, v in enumerate(list_added_to_data1):

            if i in v:

                list_index_changed_in_added_to.append(k)

            else:

                pass

    # get the changed data
    list_changed_in_data1 = [list_added_to_data1[i] for i in list_index_changed_in_added_to]

    # delete the changed in the added to data1
    list_index_changed_in_added_to = sorted(list_index_changed_in_added_to, reverse=True)

    for i in list_index_changed_in_added_to:

        del list_added_to_data1[i]

    # update the search key
    list_key = []

    for i in range(0, len(list_changed_in_data1)):

        str_temp = list_changed_in_data1[i]

        # find the positions of the delimiter
        list_pos = [j.start() for j in re.finditer(str_delimiter, str_temp)]

        str_temp = str_temp[:list_pos[int_delimiter_index]+1]

        list_key.append(str_temp)

    # search for the changed in the added to data1
    # store the indices
    list_index_changed_in_removed_from = []

    for i in list_key:

        for k, v in enumerate(list_removed_from_data1):

            if i in v:

                list_index_changed_in_removed_from.append(k)

            else:

                pass

    # delete the changed in the removed from data1
    list_index_changed_in_removed_from = sorted(list_index_changed_in_removed_from, reverse=True)

    for i in list_index_changed_in_removed_from:

        del list_removed_from_data1[i]

    # add status
    for i in range(0, len(list_removed_from_data1)):

        list_removed_from_data1[i] = str_status_rmed + str_delimiter + list_removed_from_data1[i]

    for i in range(0, len(list_added_to_data1)):

        list_added_to_data1[i]     = str_status_added + str_delimiter + list_added_to_data1[i]

    for i in range(0, len(list_changed_in_data1)):

        list_changed_in_data1[i]   = str_status_chnged + str_delimiter + list_changed_in_data1[i]

    list_data = list_removed_from_data1 + list_added_to_data1 + list_changed_in_data1

    if bool_sort:

        list_data = listNaturalSort(list_data)

    else:

        pass

    list_header = ['Status'] + list_header

    str_header = str_delimiter.join(list_header) + '\n'

    list_data = [str_header] + list_data

    if str_path_out:

        with open(str_path_out, 'w+') as fout:

            for i in list_data:

                fout.write(i)
        
    else:

        if bool_sort:

            list_added_to_data1     = listNaturalSort(list_added_to_data1)
            list_changed_in_data1   = listNaturalSort(list_changed_in_data1)
            list_removed_from_data1 = listNaturalSort(list_removed_from_data1)

        else:

            pass

        return (list_added_to_data1, list_changed_in_data1, list_removed_from_data1)
# =============================================================================
# </Function: To diff two CSVs>
# =============================================================================