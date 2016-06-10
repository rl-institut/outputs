# -*- coding: utf-8 -*-

"""
General description:
---------------------

The example models the following energy system:

                input/output  bgas     bel
                     |          |        |       |
                     |          |        |       |
 wind(FixedSource)   |------------------>|       |
                     |          |        |       |
 pv(FixedSource)     |------------------>|       |
                     |          |        |       |
 rgas(Commodity)     |--------->|        |       |
                     |          |        |       |
 demand(Sink)        |<------------------|       |
                     |          |        |       |
                     |          |        |       |
 pp_gas(Transformer) |<---------|        |       |
                     |------------------>|       |
                     |          |        |       |
 storage(Storage)    |<------------------|       |
                     |------------------>|       |


"""

###############################################################################
# imports
###############################################################################
import matplotlib.pyplot as plt
import pandas as pd
import logging

# import solph module to create/process optimization model instance
from oemof.solph import predefined_objectives as predefined_objectives

# Outputlib
from oemof.outputlib import to_pandas as tpd

# Default logger of oemof
from oemof.tools import logger


# import oemof base classes to create energy system objects
from oemof.core import energy_system as es
from oemof.core.network.entities import Bus
from oemof.core.network.entities.components import sinks as sink
from oemof.core.network.entities.components import sources as source
from oemof.core.network.entities.components import transformers as transformer


# Define logger
logger.define_logging()

###############################################################################
# read data from csv file and set time index
###############################################################################

logging.info('Read data from csv file and set time index')
data = pd.read_csv("energysystem_data.csv", sep=",")

residual = data['demand_el'] - (data['wind']*1000000 + data['pv']*582000)
positive = residual.where(residual > 0, 0)
negative = residual.where(residual < 0, 0)
print(positive.sum())
print(negative.sum())
print('len', len(negative.nonzero()[0]))

time_index = pd.date_range('1/1/2012', periods=8760, freq='H')

###############################################################################
# initialize the energy system
###############################################################################

logging.info('Initialize the energy system')
simulation = es.Simulation(
    timesteps=range(len(time_index)), verbose=True, solver='gurobi',
    objective_options={'function': predefined_objectives.minimize_cost},
    debug=True)


energysystem = es.EnergySystem(time_idx=time_index, simulation=simulation)

###############################################################################
# set optimzation options for storage components
###############################################################################

transformer.Storage.optimization_options.update({'investment': True})

###############################################################################
# Create oemof object
###############################################################################

logging.info('Create oemof objects')

grid_share = 0.1

# create gas bus
bgas = Bus(uid="bgas",
           balanced=True,
           excess=False)

bbiogas = Bus(uid="bbiogas",
              balanced=True,
              excess=False)

# create electricity bus
bel = Bus(uid="bel",
          excess=True)

# create commodity object for gas resource
rgas = source.Commodity(uid='rgas',
                        outputs=[bgas],
                        sum_out_limit=data['demand_el'].sum()/0.58*grid_share)

print(data['demand_el'].sum())

rbiogas = source.Commodity(uid='rbiogas',
                           outputs=[bbiogas],
                           sum_out_limit=1459000000)

# create fixed source object for wind
wind = source.FixedSource(uid="wind",
                          outputs=[bel],
                          val=data['wind'],
                          out_max=[1000000],
                          add_out_limit=0,
                          capex=1000,
                          opex_fix=20,
                          lifetime=25,
                          crf=0.08)

# create fixed source object for pv
pv = source.FixedSource(uid="pv",
                        outputs=[bel],
                        val=data['pv'],
                        out_max=[582000],
                        add_out_limit=0,
                        capex=900,
                        opex_fix=15,
                        lifetime=25,
                        crf=0.08)

bhkw = transformer.Simple(uid='bhkw',
                          inputs=[bbiogas], outputs=[bel],
                          out_max=[63290],
                          add_out_limit=0,
                          eta=[0.38])

# create simple sink object for demand
demand = sink.Simple(uid="demand", inputs=[bel], val=data['demand_el'])

# create simple transformer object for gas powerplant
pp_gas = transformer.Simple(uid='pp_gas',
                            inputs=[bgas], outputs=[bel],
                            opex_var=0, out_max=[10e10], eta=[0.58])

# create storage transformer object for storage
storage = transformer.Storage(uid='sto_simple',
                              inputs=[bel],
                              outputs=[bel],
                              eta_in=1,
                              eta_out=0.8,
                              cap_loss=0.00,
                              opex_fix=0,
                              opex_var=1,
                              capex=375,
                              cap_max=0,
                              c_rate_in=1/6,
                              c_rate_out=1/6,
                              lifetime=10,
                              wacc=0.07)

###############################################################################
# Optimise the energy system and plot the results
###########################################################################
logging.info('Optimise the energy system')

# If you dumped the energysystem once, you can skip the optimisation with '#'
# and use the restore method.
# energysystem.optimize()
#
# energysystem.dump()
energysystem.restore()

# Getting a results data frame
myplot = tpd.DataFramePlot(energy_system=energysystem)

storage_soc = myplot.slice_by(bus_uid='bel',
                              type='other', obj_uid='sto_simple',
                              date_from="2012-01-01 00:00:00",
                              date_to="2012-12-31 23:00:00")

pp_gas = myplot.slice_by(bus_uid="bel",
                         type='input', obj_uid='pp_gas',
                         date_from="2012-01-01 00:00:00",
                         date_to="2012-12-31 23:00:00")

demand = myplot.slice_by(bus_uid="bel",
                         type='output', obj_uid='demand',
                         date_from="2012-01-01 00:00:00",
                         date_to="2012-12-31 23:00:00")

wind = myplot.slice_by(bus_uid="bel",
                       type='input', obj_uid='wind',
                       date_from="2012-01-01 00:00:00",
                       date_to="2012-12-31 23:00:00")

pv = myplot.slice_by(bus_uid="bel",
                     type='input', obj_uid='pv',
                     date_from="2012-01-01 00:00:00",
                     date_to="2012-12-31 23:00:00")

bhkw = myplot.slice_by(bus_uid="bel",
                       type='input', obj_uid='bhkw',
                       date_from="2012-01-01 00:00:00",
                       date_to="2012-12-31 23:00:00")

print('pp_gas_sum: ', pp_gas.sum())
print('demand_sum: ', demand.sum())
print('demand_max: ', demand.max())
print('wind_sum: ', wind.sum())
print('wind: ', wind.max())
print('pv_sum: ', pv.sum())
print('pv_max: ', pv.max()/0.7647)
print('biogas_pot: ', bhkw.sum()/0.38)
