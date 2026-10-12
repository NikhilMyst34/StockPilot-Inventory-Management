from collections import deque
def search_by_sku(products,sku): return next((p for p in products if p.sku.lower()==(sku or '').strip().lower()),None)
def binary_search_by_name(products,name):
 target=name.lower(); lo=0; hi=len(products)-1
 while lo<=hi:
  mid=(lo+hi)//2; cur=products[mid].name.lower()
  if cur==target:return products[mid]
  if cur<target:lo=mid+1
  else:hi=mid-1
 return None
def sort_products(products,field='name'): return sorted(products,key=lambda p:getattr(p,field,None) or 0,reverse=field in ('quantity','selling_price'))
class StockRequestQueue:
 def __init__(self): self.items=deque()
 def enqueue(self,item): self.items.append(item)
 def dequeue(self): return self.items.popleft() if self.items else None
 def __len__(self): return len(self.items)
class UndoStack:
 def __init__(self): self.items=[]
 def push(self,item): self.items.append(item)
 def pop(self): return self.items.pop() if self.items else None
