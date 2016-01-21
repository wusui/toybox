#!/usr/bin/env python
"""
Generate all the pentomino layouts used by solving programs.  The general
algorithm will search for available squares, left to right first, then
top to bottom.  So all pentomino layouts will be oriented such that the
leftmost squares will be in column 0, and inside column 0 the topmost
square will be in row 0.  The public interface to this module,
get_layouts, will return all 63 possible pentomino layouts.
"""
import itertools

#
# Create the data structures used by get_layouts
#
gen_node = lambda xy_points : {'loc': xy_points, 'kids': [], 'mdata': []}
trav_root = lambda root_node, func_list : trav_tree({'node': root_node, 
                                                     'stack': [], 'odata': [],
                                                     'extras': [], 
                                                     'func': func_list})
#
# Main tree traversal program used by get_layouts
#
trav_tree = lambda node_info: \
    node_info['stack'].append(node_info['node']) or \
    (not node_info['node']['kids'] and
        [func(node_info) for func in node_info['func']]) or \
    ([trav_tree({'node': entry, 'stack': node_info['stack'],
                 'extras': node_info['extras'],
                 'odata': node_info['odata'], 'func': node_info['func']})
                 and node_info['stack'].pop()
                 for entry in node_info['node']['kids']]) or \
    node_info['odata']

#
# Utility function
#
map_stack = lambda node_info : map(lambda x : x['loc'], node_info['stack'])

#
# Second function executed during the initialization pass of the tree 
#
build_row = lambda node_info : [br_for_each_point(point, node_info
                                         ) for point in map_stack(node_info)]
br_for_each_point = lambda point, node_info : [br_adjust(point, adjust, \
                                                         node_info) \
                                 for adjust in [[0,1],[1,0],[0,-1],[-1,0]]]
br_adjust = lambda point, adjust, node_info : br_tests([sum(x) for x in
                                                       zip(point, 
                                                       adjust)], node_info)
br_tests = lambda new_pt, node_info : new_pt in map_stack(node_info) or \
                              new_pt[0] < 0 \
                      or (new_pt[0] == 0 and new_pt[1] < 0) or \
                      br_add_node(node_info['node'], new_pt)
br_add_node = lambda parent_node, child_loc : parent_node['kids'].append(
                    gen_node(child_loc))

#
# First function executed during the second pass of the tree
#
save_paths = lambda node_info : node_info['extras'].append(map_stack(node_info))

#
# Second function executed during the second pass of the tree
#
mark_dups = lambda node_info : md_inner(map_stack(node_info), node_info)
md_inner = lambda our_stack, node_info : \
    ([md_chkdup(our_stack, node_info, past_stack) \
             for past_stack in node_info['extras'][:-1]] or True) and \
    md_collect(our_stack, node_info)
md_chkdup = lambda our_stack, node_info, past_stack : \
    [i for i in our_stack if i in past_stack] == our_stack and \
        node_info['node']['loc'].append(-100)
md_collect = lambda our_stack, node_info : len(our_stack) == 5 and \
            -100 not in list(itertools.chain.from_iterable(our_stack)) and \
            node_info['node']['mdata'].append(our_stack)

#
# Once the tree is generated, collect the sets of point representing
# pentomino layouts
#
collect_layouts = lambda node_info, accumulator : \
    (node_info['mdata'] and accumulator.append(node_info['mdata'][0])) or \
    [collect_layouts(entry, accumulator) for entry in node_info['kids']] \
    and accumulator

#
# Wrapper to call functions for each level of the tree being built.
#
get_layouts = lambda : ly_loop(gen_node([0,0]))
ly_loop = lambda troot : [trav_root(troot, [build_row]) and \
                    trav_root(troot, [save_paths, mark_dups]) \
                    for _ in range(0,4)] and collect_layouts(troot, [])

#
# Docstrings
#
gen_node.__doc__ = \
"""
Generate a node used in the mapping of a pentomino square.
Called by br_add_node and get_layouts when creating new nodes
in the tree.
input: xy_points -- two item list representing the x and y coordinates
                    of a square.
returns: Dictionary description of the point:
            loc: the x and y location of the point.
            kids: list of child nodes of this point in the
                  pentomino generating tree
            mdata: meta-data stored for this node
"""

trav_root.__doc__ = \
"""
Generate a node_info dictionary and pass it to trav_tree.
Called from ly_loop to generate the tree from which the layout list is
extracted, and to mark duplicate layouts found.
input: root_node -- root of the tree to be traversed
       func_list -- list of functions to be executed upon each of
                    the leaf nodes in the tree.
returns: Dictionary describing a node_point:
         node -- node defined by gen_node
        stack -- list of previous node locations in the path from
                 the leaf to the root
       extras -- local data (used save stack values)
        odata -- Return data.  Mostly  used for lists of points
                 making a pentomino using the nodes in this nodes path
                 up the tree.
         func -- List of functions to be executed (passed from
                 func_list)
"""

trav_tree.__doc__ = \
"""
Recursively traverse the get_layouts tree.  Called by trav_root.
input: node_info -- node information set by either previous trav_tree
       calls or by trav_root.
returns: node_info.odata -- information set by the function routines
       passed to trav_tree.
The general flow here is:
    Set this node on the stack.
    Execute the function passed on all nodes if this is a leaf node on
    the tree.
    Recursively call trav_tree for children nodes, if they exist.
    Pop the node off the stack upon return from trav_tree.
    Return the odata field
"""

map_stack.__doc__ = \
"""
Given a node, return a list of location points in the path of the tree
to this node. Called from build_row, br_tests, save_path, and
mark_dups.
input: node_info: Node dictionary (generated by trav_root).
returns: list of location points.
"""

build_row.__doc__ = \
"""
Add a row to the tree.  Calls br_for_each_point for every point in the
figure so far.  When finished, new nodes will be added to the tree
as a next generation.
input: node_info -- Bottom node on a branch of the tree
"""

br_for_each_point.__doc__ = \
"""
For each point, assign new square along each compass point direction.
Calls br_adjust.
input:     point -- point along the path of this branch.
       node_info -- Bottom node on a branch of the tree.  
"""

br_adjust.__doc__ = \
"""
Generate a new point by adding the adjustment value to a previous point.
Calls br_test.
input:     point -- point along the path of this branch.
          adjust -- Offset added to point to find a new square.
       node_info -- Bottom node on a branch of the tree.
"""

br_tests.__doc__ = \
"""
If the new point is valid, call br_add_node to add a new node to the
tree.  A node is valid if it is not in a negative column, not in a
negative row if the column is 0, and not previously found in the figure.
input:    new_pt -- The location of the new point.
       node_info -- Bottom node on a branch of the tree.
"""

br_add_node.__doc__ = \
"""
Add a new node to the tree.
input: parent_node -- Node to which new node will be attached (as
                      a child node).
         child_loc -- location of the new node to be added to the
                      kids list for the previous node.
"""

save_paths.__doc__ = \
"""
Place the current pentomino figure's layout into the extras field of the
node.  This is set so that mark_dups can find all previous figures.
input: node_info -- Bottom node on a branch of the tree
"""

mark_dups.__doc__ = \
"""
Call md_innner with the path of this node (gotten from map_stack).
When mark_dups returns, all leaf nodes whose pentomino paths
correspond to a previous path will be marked (last node coordinates
will have a -100 value appended to it).
input: node_info -- Bottom node on a branch of the tree
"""

md_inner.__doc__ = \
"""
Call md_chkdup to see if a previously scanned path also corresponds
to this figure.  Mark node if duplicate.  Call md_collect
to save this information.
input: our_stack -- Set of parent nodes in this figures path back
                    to the root.
       node_info -- Bottom node on the branch of a tree.
"""

md_chkdup.__doc__ = \
"""
Append a -100 if the figure corresponding to this node is already
represented by a node earlier in the tree.
input: our_stack -- Set of parent nodes in this figures path back
                    to the root.
       node_info -- Bottom node on the branch of a tree.
      past_stack -- List of all previous stacks (used to find
                    duplicates)
"""

md_collect.__doc__ = \
"""
Set the mdata value in this node to be the stack if this is last node
needed for a unique complete pentomino.
input: our_stack -- Set of parent nodes in this figures path back
                    to the root.
       node_info -- Bottom node on the branch of a tree.
"""

collect_layouts.__doc__ = \
"""
Scan the node tree and find all figures saved in mdata.
input: node_info -- First node in the tree.
     accumulator -- Empty list used to save values.
returns: list of layouts of pentominos
"""

get_layouts.__doc__ = \
"""
Call ly_loop with the root node (0, 0) of a tree.
returns -- output from ly_loop call
"""

ly_loop.__doc__ = \
"""
First use build_root to generate a new row of nodes.  Then call
save_paths and mark_dups to find duplicate paths.  Repeat this
four times and all paths from leaf nodes to the root will
correspond to pentomino layouts.  Use collect_layouts to return
these paths in list form. 
input: troot -- root of the tree (node (0,0)).
returns: output from collect_layout (a list pentomino layouts)
"""

#
# Unit test non-functional calls
#
if __name__ == '__main__':
    x = get_layouts()
    print len(x)
    print x
