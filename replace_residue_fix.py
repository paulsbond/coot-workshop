def original_imol():
  for i in molecule_number_list():
    if valid_model_molecule_qm(i):
      name = residue_name(i, "A", 335, "")
      if name == "TYR":
        return i

def mlz_imol():
  for i in molecule_number_list():
    if valid_model_molecule_qm(i):
      if molecule_name(i) == "MLZ_from_dict":
        return i

def fix():
  imol = original_imol()
  if imol is None: return "Cannot find original imol"
  imol2 = mlz_imol()
  if imol2 is None: return "Cannot find MLZ imol"
  delete_residue(imol, "A", 189, "")
  delete_residue(imol, "A", 189, "")
  merge_molecules([imol2], imol)
  close_molecule(imol2)
  change_chain_id(imol, "A", "B", True, 401, 401)
  change_residue_number(imol, "B", 401, "", 189, "")
  add_terminal_residue(imol, "A", 190, "SER", 1)
  imap = imol_refinement_map()
  residues = [["A", 188, ""], ["A", 189, ""], ["A", 190, ""]]
  with AutoAccept():
    refine_residues_py(imol, residues)
    auto_fit_best_rotamer(189, "", "", "A", imol, imap, 1, 0.10)
    refine_residues_py(imol, residues)

error = fix()
if error is not None:
  print("FIX ERROR: %s" % error)
