import os
import time
import sys
import pandas as pd
import math
# تعريف الصفحة
class Node:
    def __init__(self, attribute=None, children=None, leaf=None):
        self.attribute = attribute # السمة المستخدمة في التقسيم
        self.children = children # قاموس يربط قيم السمات بأعقاد الأنواع
        self.leaf = leaf # تتحمل تسمية الصفحة (للصفحات فقط)
# تعريف الدالة ID3
def ID3(examples, target_attribute, attributes):
    # إنشاء الصفحة الأساسية
    root = Node()

    # إذا كانت جميع الأمثلة لديها نفس تسمية فئة، فإنه يجب إرجاع صفحة يحمل هذه التسمية
    if len(examples[target_attribute].unique()) == 1:
        root.leaf = examples[target_attribute].iloc[0]
        return root

    # إذا لم تتبقى سمات للانقسام، فإنه يجب إرجاع صفحة يحمل تسمية الفئة الأكثر شيوعًا
    if len(attributes) == 0:
        root.leaf = examples[target_attribute].value_counts().idxmax()
        return root

    # في هذه الحالة، يجب تحديد أفضل سمة للاستخدام في الانقسام
    best_attribute = choose_best_attribute(examples, target_attribute, attributes)
    root.attribute = best_attribute

    # إنشاء الأعقاد وبناء الشجرة بشكل متكرر
    root.children = {}
    for value in examples[best_attribute].unique():
        child_examples = examples[examples[best_attribute] == value]
        if len(child_examples) == 0:
            root.children[value] = Node(leaf=examples[target_attribute].value_counts().idxmax())
        else:
            child_attributes = [a for a in attributes if a != best_attribute]
            root.children[value] = ID3(child_examples, target_attribute, child_attributes)

    return root

# تعريف الدالة لتحديد أفضل سمة للاستخدام في الانقسام
def choose_best_attribute(examples, target_attribute, attributes):
    best_attribute = None
    max_gain = -float("inf")

    for attribute in attributes:
        gain = information_gain(examples, target_attribute, attribute)
        if gain > max_gain:
            max_gain = gain
            best_attribute = attribute

    return best_attribute

# تعريف الدالة لحساب الفائدة المعلوماتية لسمة معينة
def information_gain(examples, target_attribute, attribute):
    entropy_before = entropy(examples[target_attribute])
    entropy_after = 0
    for value in examples[attribute].unique():
        child_examples = examples[examples[attribute] == value]
        entropy_after += len(child_examples) / len(examples) * entropy(child_examples[target_attribute])

    return entropy_before - entropy_after

# تعريف الدالة لحساب الانحراف المعياري لسمة معينة
def entropy(target_attribute):
    entropy = 0
    for value in target_attribute.unique():
        p = len(target_attribute[target_attribute == value]) / len(target_attribute)
        entropy -= p * math.log(p, 2)
    return entropy

def display_tree(node, level,target_attribute):
    """
    Display the decision tree starting from the given node.
    """
    prefix = "\t" * level
    if node.leaf is not None:
        print(prefix + target_attribute +'['+ str(node.leaf)+ ']')
        return
    print(prefix + '(' + node.attribute +')')
    for value, child_node in node.children.items():
        print(prefix + '\t' + value + " -> ", end="")
        display_tree(child_node, level + 1,target_attribute)
def print_rules(node, rule,target_attribute):
    
    # قم بتوليد الشروط من العقدة الحالية
    if node.leaf is not None:
        # قم بإرجاع النتيجة عندما تصل إلى ورقة
        print('IF ' + rule + ' THEN ' + target_attribute + ' = ' + str(node.leaf))
        return
    # تحديد عدد العقد الفرعية
    num_subnodes = len(node.children)

    # تكرار على كل عقد فرعي
    for value, child_node in node.children.items():
        subrule = rule
        if subrule:
            subrule += ' AND '
        subrule += '(' + str(node.attribute) + ' = ' + str(value) + ')'
        print_rules(child_node, subrule,target_attribute)
def predict(node, record):
    if node.leaf is not None:
        return node.leaf
    attribute_value = record[node.attribute]
    if attribute_value not in node.children:
        return None
    child_node = node.children[attribute_value]
    return predict(child_node, record)


class minID3:
    def __init__(self,examples,attributes,target_attribute,record_dict):
        self.examples = examples
        self.attributes=attributes
        self.target_attribute = target_attribute
        self.record_dict=record_dict
    def minID3(self):
        print('\t*10 مرحبا بكم في تطبيق خوارزمية شجرة القرار ID3')
        # تنفيذ الخوارزمية وعرض الشجرة الناتجة
        root = ID3(self.examples, self.target_attribute, [a for a in self.attributes if a != self.target_attribute])
        #الخطوة الرابعة طباعة الشحرة
        if input('Do you print of tree?(y/n):')=='y':
            print('The Decision Tree for Dataset:')
            display_tree(root,0,self.target_attribute)
       #الخطوة الخامسة استخراج القواعد المكتشفة من الشجرة
        if input('Do you print of Model (Rules) of the Tree?(y/n):')=='y':
            print('The Model (Rules) of the Tree are:')
            print_rules(root, '',self.target_attribute)
        predicted_class = predict(root, self.record_dict)
        print('The predicted class for the new record is:', predicted_class)    
       
