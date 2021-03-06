### Game of life
If not sure what it is, check: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life <br />
There are two implementations: with and without classes

### Tests results:
  #### 1 part of work (no classes)
  
```python
test_can_create_a_random_grid (__main__.TestGameOfLife) ... ok
test_can_create_an_empty_grid (__main__.TestGameOfLife) ... ok
test_can_update (__main__.TestGameOfLife) ... ok
test_get_neighbours (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_bottom_side (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_left_side (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_lower_left_corner (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_lower_right_corner (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_right_side (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_upper_left_corner (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_upper_right_corner (__main__.TestGameOfLife) ... ok
test_get_neighbours_for_upper_side (__main__.TestGameOfLife) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.046s

OK 
```

#### 2 part (with classes)

```python
test_can_create_a_cell (__main__.TestCell) ... ok
test_can_create_a_grid_from_file (__main__.TestCellList) ... ok
test_can_create_a_random_grid (__main__.TestCellList) ... ok
test_can_create_an_empty_grid (__main__.TestCellList) ... ok
test_can_iterate_over_clist (__main__.TestCellList) ... ok
test_can_update (__main__.TestCellList) ... ok
test_clist_is_iterable (__main__.TestCellList) ... ok
test_get_neighbours (__main__.TestCellList) ... ok
test_get_neighbours_for_bottom_side (__main__.TestCellList) ... ok
test_get_neighbours_for_left_side (__main__.TestCellList) ... ok
test_get_neighbours_for_lower_left_corner (__main__.TestCellList) ... ok
test_get_neighbours_for_lower_right_corner (__main__.TestCellList) ... ok
test_get_neighbours_for_right_side (__main__.TestCellList) ... ok
test_get_neighbours_for_upper_left_corner (__main__.TestCellList) ... ok
test_get_neighbours_for_upper_right_corner (__main__.TestCellList) ... ok
test_get_neighbours_for_upper_side (__main__.TestCellList) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.054s

OK
