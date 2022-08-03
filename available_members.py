# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------------
# Name:       available_members.py
# Purpose:    DelphiVCL for Python sample
#
# Author:     Nestor D R
# Version:    0.0.1
#
# Copyright:  2020-2022 Embarcadero Technologies, Inc.
# License:    https://github.com/Embarcadero/DelphiVCL4Python/blob/main/LICENSE.md
# ---------------------------------------------------------------------------------

# --- Third Party libraries ---
# delphivcl: Delphi's VCL library as a Python module for building native Windows GUI Applications
import delphivcl

# To view a list of all exposed members
list_ = dir(delphivcl)
print("All exposed members by Delphi VCL")
print(list_)

# To view the exposed members, by slice
slice_size_ = 12
print("\n\nExposed members by Delphi VCL, in slices")
for i in range(0, len(list_), slice_size_):
    print(list_[i:i+slice_size_])

# To view the exposed sub-members for a main member, by slice
print("\n\nExposed sub-members for a main Delphi VCL member, in slices")
list_ = dir(delphivcl.ComboBox)
for i in range(0, len(list_), slice_size_):
    print(list_[i:i+slice_size_])
