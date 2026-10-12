import unittest
from types import SimpleNamespace
from dsa import search_by_sku,binary_search_by_name,sort_products,StockRequestQueue,UndoStack
class Tests(unittest.TestCase):
 def setUp(self): self.p=[SimpleNamespace(name="Cable",sku="A-3",quantity=8,selling_price=199),SimpleNamespace(name="Mouse",sku="A-1",quantity=2,selling_price=499),SimpleNamespace(name="Notebook",sku="B-2",quantity=20,selling_price=60)]
 def test_sku(self): self.assertEqual(search_by_sku(self.p,"a-1").name,"Mouse")
 def test_binary(self): self.assertEqual(binary_search_by_name(sorted(self.p,key=lambda x:x.name.lower()),"notebook").name,"Notebook")
 def test_sort(self): self.assertEqual(sort_products(self.p,"quantity")[0].quantity,20)
 def test_queue(self): q=StockRequestQueue();q.enqueue(1);q.enqueue(2);self.assertEqual(q.dequeue(),1)
 def test_stack(self): s=UndoStack();s.push(1);s.push(2);self.assertEqual(s.pop(),2)
if __name__=='__main__':unittest.main()
