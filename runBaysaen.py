class Baysaen:
    def __init__(self,examples,attributes,target_attribute,record_dict):
        self.examples = examples
        self.attributes=attributes
        self.target_attribute = target_attribute
        self.record_dict=record_dict
        self.maxClass=None
    def predict_class(self):
        # حساب عدد السجلات في الجدول
        countAll = len(self.examples)
        print("#" * 50)
        print(f"The count of all records: {countAll}")
        print("#" * 50)

        # حساب احتمالية كل قيمة في target_attribute
        target_values = self.examples[self.target_attribute].value_counts(normalize=True).round(3).to_dict()
        print(f"Probability of each value in the Class({self.target_attribute}):")
        for value, pClass in target_values.items():
            print(f"\t{value}: {pClass}")

        # حساب احتمالية كل جزء من السجل الجديد لكل كلاس
        new_values = {nameClass: 1 for nameClass in target_values}
        print("#" * 50)
        print("Step 2:")
        print('\t','|',' ' * 2,'Attribute',' ' * 2,'|',' ' * 2,'Value',' ' * 2,'|',' ' * 2,'Class',' ' * 10,'|')
        print('\t','-' * 55)
        values_str = [str(value) for value in target_values]
        values_str = '              '.join(values_str)
        print('\t',' ' * 31,'|',f'{values_str.strip()}')
        print('\t',' ' * 31,'-' * 24)
        for attribute, valueNew in self.record_dict.items():
            print('\t','|',' ' * 2,f'{attribute}',' ' * (11-len(attribute)),'|',' ' * 2,f'{valueNew}',' ' * (7-len(valueNew)),'',end='')
            child = self.examples[self.examples[attribute] == valueNew]
            
            #print('\t',' ' * 31,'-' * 22)
            for classValue in target_values:
                countValueCalse = child[self.target_attribute].value_counts().get(classValue, 0)
                countClass = self.examples[self.target_attribute].value_counts().get(classValue, 0)
                PValueCalss = countValueCalse / countClass if countClass != 0 else 0
                new_values[classValue] *= PValueCalss
                print('|' ,f'{countValueCalse}/{countClass} = {round(PValueCalss, 3)}',end='')
                
            print('\n\t','-' * 55)

        # حساب احتمالية الكلاسات النهائية
        class_probabilities = {nameClass: target_values[nameClass] * new_values[nameClass] for nameClass in new_values}
        print("#" * 50)
        print("Step 3:")
        for nameClass, pClass in class_probabilities.items():
            print(f"Class = {nameClass}: {pClass:.5f}")

        # تحديد الكلاس الأكثر احتمالاً
        print("#" * 50)
        print("Step 4:")
        maxClass = max(class_probabilities, key=class_probabilities.get)
        print(f"Predicted class: {maxClass}")
        return self.maxClass
