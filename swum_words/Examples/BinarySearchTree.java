package com.gradescope.hw09;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;
import java.util.Set;

/**
 * BinarySearchTree
 *
 * An Unbalanced Binary Search Tree, which implements the Map interface (i.e.
 * maps between keys and values). The user specifies the type of the keys and
 * the type of the values. The type of the keys must be a type that implements
 * the interface Comparable.
 */
public class BinarySearchTree<KeyType extends Comparable<KeyType>, ValueType>
        implements Map<KeyType, ValueType> {

    /** a reference to the root of the tree (null if the tree is empty) **/
    BSTNode rootNode;
	private int treeSize;

    public BinarySearchTree() {
        this.rootNode = null;
    }

    /**
     * BSTNode
     *
     * Private inner class BSTNode represents the nodes of the BST, with each
     * BSTNode storing a key, a value, and references to the left and right
     * subtrees.
     */
    private class BSTNode {
        // NOTE: BSTNode has only fields and constructors
        private KeyType key;
        private ValueType value;
        private BSTNode leftTree;
        private BSTNode rightTree;

        private BSTNode(KeyType inputKey, ValueType inputValue) {
            if (inputKey == null || inputValue == null) {
                throw new IllegalArgumentException(
                        "Inserted keys and values must be non-null");
            }
            this.key = inputKey;
            this.value = inputValue;
            this.leftTree = null;
            this.rightTree = null;
        }

        private BSTNode(KeyType inputKey, ValueType inputValue,
                BSTNode inputLeftT, BSTNode inputRightT) {
            this(inputKey,inputValue);
            this.leftTree = inputLeftT;
            this.rightTree = inputRightT;
        }
    }

    // //////////////////////////////////////////////////////////////////
    // *** Queries about the tree ***
    // Methods: isEmpty, size, containsKey, containsValue,
    //          get, getMinKey, height
    // //////////////////////////////////////////////////////////////////

    public boolean isEmpty() {
        return this.rootNode == null;
    }

    /*
     * @see java.util.Map#size()
     */
    public int size() {
    	if (this.rootNode == null) {
            return 0;
        }
        return this.treeSize;
    }

    /*
     * @see java.util.Map#containsKey(java.lang.Object)
     */
    public boolean containsKey(Object keyToFind) {
        return this.get(keyToFind) != null;
    }
    /*
     * @see java.util.Map#containsValue(java.lang.Object)
     */
    public boolean containsValue(Object value) {
        // search through all keys
        for (KeyType key : this.getAllKeysInOrder()) {
            ValueType oneValue = get(key);
            if (oneValue.equals(value)) {
                return true;
            }
        }

        return false; // key not found
    }
    /*
     * @see java.util.Map#get(java.lang.Object)
     */
    @SuppressWarnings("unchecked")
    public ValueType get(Object key) {
        return get((KeyType) key, this.rootNode);
    }

    /**
     * private, recursive helper method to perform get
     *
     * @param keyToFind
     *            the key we're searching for
     * @param tempRoot
     *            the root of the tree in which we're searching
     * @return the value associated with the key (or null if key is not in tree)
     */
    private ValueType get(KeyType keyToFind, BSTNode tempRoot) {
        // base case: empty tree
        if (tempRoot == null) {
            return null;
        }

        KeyType currentKey = tempRoot.key;

        // base case: found the key
        if (keyToFind.equals(currentKey)) {
            return tempRoot.value;
        }

        // if keyToFind < currentKey, then search the left subtree
        else if (inOrderKeys(keyToFind, currentKey)) {
            return get(keyToFind, tempRoot.leftTree);
        }

        // if currentKey < keyToFind, then search the right subtree
        else {
            return get(keyToFind, tempRoot.rightTree);
        }
    }

    /**
     * Finds the minimum key in the tree. If the tree is empty, throws an
     * IllegalArgumentException.
     *
     * @return the value of the smallest key in the tree
     */
    public KeyType getMinKey() throws IllegalArgumentException {
       if(isEmpty()) {
    	   throw new IllegalArgumentException();
       }
        return getMinKey(this.rootNode);
    }

    /**
     * Private helper method that recursively finds the minimum key in a
     * non-empty tree.
     *
     * @param tempRoot the root of the non-empty tree
     * @return the value of the smallest key in the tree
     */
    private KeyType getMinKey(BSTNode tempRoot) {
		if(tempRoot.leftTree==null) {
			return tempRoot.key;
		}
		else {
			return getMinKey(tempRoot.leftTree);
		}
	}

    /**
     * Returns the height of the tree, where height is the maximum number of
     * edges between the root and a leaf.
     *
     * The height of an empty tree is -1.
     *
     * @return the tree's height
     */
    public int getHeight() {
        return getHeight(this.rootNode);
    }

    /**
     * Private helper method that recursively finds the height of a tree
     *
     * @param tempRoot
     *            the root of the tree
     * @return the height of the tree rooted at the given node
     */
    private int getHeight(BSTNode tempRoot) {
        if (tempRoot == null) {
            return -1;
        } else {
            int leftHeight = getHeight(tempRoot.leftTree);
            int rightHeight = getHeight(tempRoot.rightTree);
            return 1 + Math.max(leftHeight, rightHeight);
        }

    }

    // //////////////////////////////////////////////////////////////////
    // *** Modifications to the tree ***
    // Methods: clear, put, putAll, remove
    // //////////////////////////////////////////////////////////////////
    /*
     * @see java.util.Map#clear()
     */
    public void clear() {
        this.rootNode = null;
    }
    /*
     * @see java.util.Map#put(java.lang.Object, java.lang.Object)
     */
    public ValueType put(KeyType key, ValueType value) {
        this.rootNode = put(key, value, this.rootNode);
        return value; // Always return the value added to the tree
    }

    /**
     * Private helper method to perform put using recursion
     *
     * @param inputKey
     *            the key to insert
     * @param inputValue
     *            the value to insert
     * @param tempRoot
     *            the root of the tree in which to insert the new key/value
     * @return the (possibly new) root of the tree
     */
    private BSTNode put(KeyType inputKey, ValueType inputValue,
            BSTNode tempRoot) {
        // base case: tree is empty, so create a new node for the root and
        //            return it
        if (tempRoot == null) {
            BSTNode newNode = new BSTNode(inputKey, inputValue);
            this.treeSize++;
            return newNode;
        }

        KeyType currentKey = tempRoot.key;

        // base case: the key is at the root, update the root with the new value
        if (inputKey.equals(currentKey)) {
            tempRoot.value = inputValue;
        }

        // if keyToFind < currentKey, then put in the left subtree
        else if (this.inOrderKeys(inputKey, currentKey)) {
            tempRoot.leftTree = put(inputKey, inputValue, tempRoot.leftTree);
        }

        // if currentKey < keyToFind, then put in the right subtree
        else {
            tempRoot.rightTree = put(inputKey, inputValue, tempRoot.rightTree);
        }

        return tempRoot;
    }
    /*
     * @see java.util.Map#putAll(java.util.Map)
     */
    public void putAll(
            Map<? extends KeyType, ? extends ValueType> mapOfNewEntries) {
        for (KeyType key : mapOfNewEntries.keySet()) {
            ValueType value = mapOfNewEntries.get(key);
            this.put(key, value);
            this.treeSize++;
        }
    }

    /*
     * @see java.util.Map#remove(java.lang.Object)
     */
    @SuppressWarnings("unchecked")
    public ValueType remove(Object key) {
        ValueType value = get(key);
        if (value != null) { // Only try to remove keys that are in the tree
            this.rootNode = remove((KeyType)key, this.rootNode);
            this.treeSize --;
            }
        return value;
    }

    /**
     * Private helper method to perform remove using recursion
     *
     * @param inputKey the key to remove
     * @param tempRoot the root of tree from which we should remove the key
     * @return a reference to the root of the (possibly) modified tree
     */

    private BSTNode remove(KeyType inputKey, BSTNode tempRoot) {
	    	if(tempRoot == null) {
	    		return tempRoot;
	    	}
	    	else if(inputKey.compareTo(tempRoot.key) < 0) {
	    		tempRoot.leftTree = remove(inputKey, tempRoot.leftTree);
	    	}
	    	else if(inputKey.compareTo(tempRoot.key) > 0) {
	    		tempRoot.rightTree = remove(inputKey, tempRoot.rightTree);
	    }
	    	else {
	    		if(tempRoot.rightTree == null && tempRoot.leftTree == null) {
	    			tempRoot = null;
	    		}
	    		else if(tempRoot.rightTree == null) {
	    			tempRoot = tempRoot.leftTree;
	    		}
	    		else if(tempRoot.leftTree == null) {
	    			tempRoot = tempRoot.rightTree;
	    		}
	    		else {
	    			BSTNode min = getMinNode(tempRoot);
	    			return new BSTNode(min.key, min.value, tempRoot.leftTree, remove(min.key, tempRoot.rightTree));
	    			}
	    		}
	    	return tempRoot;
    	}


    private BSTNode getMinNode(BSTNode tempRoot) {
		if(tempRoot.leftTree==null) {
			return tempRoot;
		}
		else {
			return getMinNode(tempRoot.leftTree);
		}
	}
    // //////////////////////////////////////////////////////////////////
    // *** Debugging Methods ***
    // Methods: printTreeStructure, toString
    // //////////////////////////////////////////////////////////////////

    /**
     * prints an indented tree structure of the BinarySearchTree
     */
    public void printTreeStructure() {
        printTreeStructure(this.rootNode, 0);
    }

    /**
     * private helper method to recursively print the tree structure
     *
     * @param currentNode the root of the tree we're printing
     * @param currentDepth the indentation level
     */
    private void printTreeStructure(BSTNode currentNode, int currentDepth) {
        if (currentNode != null) {
            String currentNodeStr = "[" + currentNode.key.toString() + " , "
                    + currentNode.value.toString() + "]";
            for (int count = 1; count <= currentDepth; count++) {
                System.out.print("\t");
            }
            System.out.println(currentNodeStr);
            printTreeStructure(currentNode.leftTree, currentDepth + 1);
            printTreeStructure(currentNode.rightTree, currentDepth + 1);
        }
    }

    /*
     * @see java.lang.Object#toString()
     */
    public String toString() {
        ArrayList<KeyType> allKeys = this.getAllKeysInOrder();
        return allKeys.toString();
    }

    // //////////////////////////////////////////////////////////////////
    // *** Helper Methods ***
    // Methods: inOrderKeys, getAllKeysInOrder
    // //////////////////////////////////////////////////////////////////
    /**
     * returns true if key1 is less than key2
     *
     * @param key1
     * @param key2
     * @return
     */
    private boolean inOrderKeys(KeyType key1, KeyType key2) {
        return key1.compareTo(key2) < 0;
    }

    /**
     * A private helper method that returns an ArrayList of all of the keys in
     * order
     *
     * @return the keys in sorted order
     */
    private ArrayList<KeyType> getAllKeysInOrder() {
    		ArrayList<KeyType> keyList = new ArrayList<KeyType>();
        addKeysToArrayList(keyList,this.rootNode);
        return keyList;
    }

    /**
     * A private, recursive helper method to create an ArrayList of keys in
     * order
     *
     * @param keyList an ArrayList that contains keys in order
     * @param currentNode the root of a tree to add keys from
     */
    private void addKeysToArrayList(ArrayList<KeyType> keyList, BSTNode currentNode) {
    		if(currentNode.key==null) {
    			return;
    		}
    		if (currentNode.leftTree == null && currentNode.rightTree == null) {
                keyList.add(currentNode.key);
            }
    		else if (currentNode.rightTree == null) {
                addKeysToArrayList(keyList, currentNode.leftTree);
                keyList.add(currentNode.key);
            }
    		else if (currentNode.leftTree == null) {
                keyList.add(currentNode.key);
                addKeysToArrayList(keyList, currentNode.rightTree);
            }
    		else {
                addKeysToArrayList(keyList, currentNode.leftTree);
                keyList.add(currentNode.key);
                addKeysToArrayList(keyList, currentNode.rightTree);
            }
        }

    // //////////////////////////////////////////////////////////////////
    // Unimplemented Methods: entrySet, keySet, values
    // //////////////////////////////////////////////////////////////////
    /*
     * @see java.util.Map#entrySet()
     */
    public Set<Entry<KeyType, ValueType>> entrySet() {
        throw new UnsupportedOperationException();
    }
    /*
     * @see java.util.Map#keySet()
     */
    public Set<KeyType> keySet() {
        throw new UnsupportedOperationException();
    }
    /*
     * @see java.util.Map#values()
     */
    public Collection<ValueType> values() {
        throw new UnsupportedOperationException();
    }
}