def matrixSolver(matrix):
	#TRANSFORMING MATRIX TO ROW ECHELON FORM (Forward Pass)
	rows = len(matrix)
	cols = len(matrix[0])
	for pivot_row in range(rows):
		pivot_col = pivot_row
		while pivot_col < cols:
			candidate_row = pivot_row
			found_pivot = False
			while candidate_row < rows:
				if matrix[candidate_row][pivot_col] != 0:
					swap_rows(matrix, candidate_row, pivot_row)
					found_pivot = True
					break
				candidate_row += 1
			if found_pivot:
				break
			pivot_col += 1
		col = pivot_col
		row = pivot_row + 1
		while row < rows:
			if matrix[row][pivot_col] == 0:
				row += 1
				continue
			q = (-1 * matrix[row][pivot_col]) / matrix[pivot_row][pivot_col]
			col = pivot_col
			while col < cols:
				matrix[row][col] += (matrix[pivot_row][col] * q)
				col += 1
			row += 1
	#MATRIX IS NOW IN ROW ECHELON FORM
	#TRANSFORMING MATRIX TO REDUCED-ROW ECHELON FORM (Backward Pass)
	scaling_row = rows - 1
	while scaling_row >= 0:
		leading_entry_col = 0
		while leading_entry_col < cols:
			if matrix[scaling_row][leading_entry_col] != 0:
				break
			leading_entry_col += 1
		if leading_entry_col == cols:
			scaling_row -= 1
			continue
		if matrix[scaling_row][leading_entry_col] != 1:
			scale_col = leading_entry_col
			denominator = matrix[scaling_row][leading_entry_col]
			while scale_col < cols:
				matrix[scaling_row][scale_col] /= denominator
				scale_col += 1
		target_row = scaling_row - 1
		while target_row >= 0:
			if matrix[target_row][leading_entry_col] == 0:
				target_row -= 1
				continue
			q = (-1 * matrix[target_row][leading_entry_col]) / matrix[scaling_row][leading_entry_col]
			target_col = leading_entry_col
			while target_col < cols:
				matrix[target_row][target_col] += (matrix[scaling_row][target_col] * q)
				target_col += 1
			target_row -= 1
		scaling_row -= 1


def swap_rows(matrix, row1_index, row2_index):
	temp = matrix[row1_index]
	matrix[row1_index] = matrix[row2_index]
	matrix[row2_index] = temp

def print_matrix(matrix):
	rows = len(matrix)
	cols = len(matrix[0])
	str_matrix = []
	for i in range(rows):
		str_row = []
		for j in range(cols):
			str_row.append(str(matrix[i][j]))
		str_matrix.append(str_row)
	str_rows = []
	for i in range(rows):
		str_rows.append(" ".join(str_matrix[i]))
	print("\n".join(str_rows))

#matrix = [
#			[1, 2, -1, 2, 1, 2],
#			[-1, -2, 1, 2, 3, 6],
#			[2, 4, -3, 2, 0, 3],
#			[-3, -6, 2, 0, 3, 9]
#		]

#matrixSolver(matrix)
#print_matrix(matrix)