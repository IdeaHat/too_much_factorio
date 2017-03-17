import math
import numpy as np
import sys
def fdiv(x, y):
  return float(x) / float(y)
def fmul(x, y):
  return float(x) * float(y)
factory_mul = 0.75
furnace_mul = 1
inserter_througput = [0.831, 2.306]
coal_energy_MJ = 8

class Factory:
  def __init__(self, name, time, dep_list, output, multiplier=factory_mul):
    self.name = name
    self.dep_list = dep_list
    self.time = fdiv(time, multiplier)
    if isinstance(output, dict):
      self.output = output
    else:
      self.output = {self.name: output}
  def get_consumption_rate(self, dep):
    return fdiv(self.dep_list.get(dep, 0), self.time)
  def get_production_rate(self, output):
    return fdiv(self.output.get(output, 0), self.time)
  def get_production_rates(self):
    return {key: self.get_production_rate(key) for key in self.output.keys()}
  def get_consumption_rates(self):
    return {key: self.get_consumption_rate(key) for key in self.dep_list.keys()}

def depth_first_search_from_node(search_index, adjacency_list, visited=[], sorted_indexed=[]):
  visited[search_index] = True
  for n in adjacency_list[search_index]:
    if not visited[n]:
       depth_first_search_from_node(n, adjacency_list, visited, sorted_indexed)
  sorted_indexed.append(search_index)
  return sorted_indexed

def depth_first_search(adjacency_list):
  visited = [False for a in range(len(adjacency_list))]
  sorted_indexed = []
  for n in range(len(adjacency_list)):
    if not visited[n]:
      depth_first_search_from_node(n, adjacency_list, visited, sorted_indexed)
  return sorted_indexed

### Set up
factories = [Factory('coal', 1/0.525, dict(), 1, 1),
  Factory('iron ore', 1/0.525, dict(), 1, 1),
  Factory('iron', 3.5, {'iron ore': 1}, 1, furnace_mul),
  Factory('copper ore', 1/0.525, dict(), 1, 1),
  Factory('copper', 3.5, {'copper ore': 1}, 1, furnace_mul),
  Factory('steel', 17.5, {'iron': 5}, 1, furnace_mul),
  Factory('gear', 0.5, {'iron': 2}, 1),
  Factory('circuit', 0.5, {'iron': 1, 'cabel':3}, 1),
  Factory('cabel', 0.5, {'copper': 1}, 2),
  # Factory('light_cracking', 5, {"light_oil": 3}, {'gas': 2}, 1),
  # Factory('heavy_cracking', 5, {"heavy_oil": 4}, {'light_oil': 3}, 1),
  Factory('belt', 0.5, {'iron': 1, 'gear': 1}, 2),
  Factory('inserter', 0.5, {'iron': 1, 'gear': 1, 'circuit': 1}, 1),
  Factory('sp1', 5, {'copper': 1, 'gear': 1}, 1),
  Factory('sp2', 6, {'inserter': 1, 'belt': 1}, 1),
  Factory('f_inserter',  0.5, {'inserter': 1, 'iron': 2, 'circuit': 2}, 1),
  Factory('s_inserter',  0.5, {'f_inserter': 1, 'circuit': 4}, 1),
  Factory('battery', 5, {'iron': 1, 'copper': 1, 'acid': 2}, 1, 1),
  Factory('adv_circuit', 8, {'circuit': 2, 'plastic': 2, 'cabel': 4}, 1),
  Factory('crude', 1, dict(), 1, 1),
  Factory('plastic', 1, {'coal': 1, 'gas': 3}, 2, 1),
  Factory('sp3', 12, {'battery': 1, 'adv_circuit': 1, 's_inserter': 1, 'steel': 1}, 1),
  Factory('engine', 20, {'steel': 1, 'gear': 1, 'pipe': 2},1),
  Factory('eengine', 20, {'engine': 1, 'circuit': 2, 'lubricant': 2}, 1),
  Factory('robot', 20, {'eengine': 1, 'battery': 2, 'steel': 1, 'circuit': 3}, 1),
  Factory('logistics', 0.5, {'robot': 1, 'adv_circuit': 2}, 1),
  Factory('pipe', 0.5, {'iron': 1}, 1),
  Factory('oil_processing', 5, {'crude': 3}, {'light_oil': 3, 'heavy_oil': 3, 'gas': 4}, 1),
  # Factory('adv_oil_processing', 5, {'crude': 10}, {'light_oil': 4.5, 'heavy_oil': 1, 'gas': 5.5}, 1),
  Factory('sulfur', 1, {'gas': 3}, 2, 1),
  Factory('acid', 1, {'sulfur': 5, 'iron': 1}, 5, 1),
  Factory('lubricant', 1, {'heavy_oil': 1}, 1, 1),
  Factory('magazine', 2, {'iron': 2}, 1),
  Factory('solar', 10, {'steel': 5, 'circuit': 15, 'copper': 5}, 1),
  Factory('processing unit', 15, {'circuit': 20, 'adv_circuit': 2, 'acid': 0.5}, 1),
  Factory('accumulator', 10, {'iron': 2, 'battery': 5}, 1),
  Factory('cannon', 8, {'steel': 4, 'plastic': 2, 'explosives': 1}, 1),
  Factory('explosives', 5, {'sulfur': 1, 'coal': 1}, 1, 1),
  Factory('piercing', 3, {'copper': 5, 'steel': 1}, 1),
  Factory('speed', 15, {'adv_circuit': 5, 'circuit': 5}, 1),
  Factory('speed_2', 30, {'adv_circuit': 5, 'processing unit': 5, 'speed':4}, 1),
  Factory('speed_3', 60, {'adv_circuit': 5, 'processing unit': 5, 'speed_2':4}, 1),
  Factory('efficiency', 15, {'adv_circuit': 5, 'circuit': 5}, 1),
  Factory('efficiency_2', 30, {'adv_circuit': 5, 'processing unit': 5, 'efficiency':4}, 1),
  Factory('efficiency_3', 60, {'adv_circuit': 5, 'processing unit': 5, 'efficiency_2':4}, 1),
  Factory('productivity', 15, {'adv_circuit': 5, 'circuit': 5}, 1),
  Factory('productivity_2', 30, {'adv_circuit': 5, 'processing unit': 5, 'productivity':4}, 1),
  Factory('productivity_3', 60, {'adv_circuit': 5, 'processing unit': 5, 'speed_2':4}, 1),
  Factory('rocket', 3, {'lds': 10, 'rocket_fuel': 10, 'control': 10}, 1, 1),
  Factory('lds', 30, {'steel': 10, 'copper': 5, 'plastic': 5}, 1),
  Factory('rocket_fuel', 30, {'solid_fuel': 10}, 1, 1),
  Factory('hsolid_fuel', 3, {'heavy_oil': 2}, {'solid_fuel': 1}, 1),
  Factory('lsolid_fuel', 3, {'light_oil': 1}, {'solid_fuel': 1}, 1),
  Factory('gsolid_fuel', 3, {'gas': 2}, {'solid_fuel': 1}, 1),
  Factory('control', 30, {'processing unit': 1, 'speed': 1}, 1)
]

if (len(sys.argv) > 1):
  l = int(sys.argv[1])
else:
  l = 0

factory_name_to_index = dict()
for i in range(len(factories)):
   factory_name_to_index[factories[i].name] = i

def saturate_factory(name, output = None):
  if output is None:
    output = name
  return factories[factory_name_to_index[name]].get_production_rate(name)

solar_rate = saturate_factory('solar')
goal_levels = [
{
  'sp1': saturate_factory('sp1')*4,
  'sp2': saturate_factory('sp1')*4,
  'magazine': saturate_factory('magazine')*1
}]
goals = goal_levels[0]

name_to_index = dict();
count = 0
for factory in factories:
  for (output, volume) in factory.output.iteritems():
    name_to_index.setdefault(output, [])
    name_to_index[output].append(count)
  count = count + 1

raws = {'iron ore','copper ore','coal', 'crude'}
outputs = sorted(list(set(sum([f.output.keys() for f in factories], []))))
outputs =  dict((outputs[i], i) for i in range(len(outputs)))

### Parse graph
dependency_graph = []

for factory in factories:
  n = [];
  for dep in factory.dep_list.keys():
    n.extend(name_to_index[dep])
  dependency_graph.append(n);

dependent_graph = [[] for a in dependency_graph]
for n in range(len(dependent_graph)):
  for m in dependency_graph[n]:
    dependent_graph[m].append(n)

## Compute rates
A = [[0 for n in range(len(factories))] for n in range(len(outputs))]

for i in range(len(factories)):
  f = factories[i]
  for (o, v) in f.get_production_rates().iteritems():
    A[outputs[o]][i] = -v
  for (c, v) in f.get_consumption_rates().iteritems():
    A[outputs[c]][i] = v

max_name = max([len(factory.name) for factory in factories])

goal_rates = [0 for o in range(len(outputs))]
for (o, v) in goals.iteritems():
  goal_rates[outputs[o]] = -v

# convert to a system of linear inequalities.
raws_i = [0.0 for f in factories]
for raw in raws:
  for r in name_to_index[raw]:
    raws_i[r] = 1.0;
    
from scipy.optimize import linprog
m2 = linprog(raws_i, A_ub=A, b_ub=goal_rates, bounds=[(0,None) for i in factories])
np_factories = m2.x
sorted_indexed = depth_first_search(dependency_graph)
if (len(sys.argv) < 3):
    fnames = sorted([f.name for f in factories]);
    for f in sorted_indexed:
      i = f
      #if np_factories[i] > 0.00:
      factory = factories[i]
      if (math.ceil(np_factories[i]) > 0):
        print ("%% %ds: %%03d (%%07.3f) | %%d" % max_name) % (factory.name, math.ceil(np_factories[i]), np_factories[i], len(dependent_graph[i]))
if (len(sys.argv) == 3):
    fname = sys.argv[2];
    factory_ind = factory_name_to_index[fname]
    factory = factories[factory_ind]
    dinds =dependent_graph[factory_ind]
    drates = [factories[d].get_consumption_rate(fname)*np_factories[d] for d in dinds]
    tot = sum(drates)
    for i in range(len(dinds)):
      if drates[i]/tot > 0.001:
        print ("%% %ds: %%0.3f" % max_name) % (factories[dinds[i]].name, drates[i]/tot)
    