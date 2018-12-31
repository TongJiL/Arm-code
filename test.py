import numpy as np

from openmdao.api import ExplicitComponent


class CosComp(ExplicitComponent):
    
    def initialize(self):
        self.options.declare('num_nodes', default=1, types=int)

    def setup(self):
        num_nodes = self.options['num_nodes']

        self.add_input('x', shape=(num_nodes, 2))
        self.add_output('y', shape=(num_nodes, 2))
        
        arange = np.arange(2 * num_nodes)
        self.declare_partials('y', 'x', rows=arange, cols=arange)

    def compute(self, inputs, outputs):
        x = inputs['x']
        outputs['y'][:, 0] = np.sin(x[:, 0])
        outputs['y'][:, 1] = np.cos(x[:, 1])

    def compute_partials(self, inputs, partials):
        x = inputs['x']
        derivs = partials['y', 'x'].reshape((num_nodes, 2))
        derivs[:, 0] = np.cos(x[:, 0])
        derivs[:, 1] = -np.sin(x[:, 1])


if __name__ == '__main__':
    from openmdao.api import Problem, IndepVarComp
    
    num_nodes = 5

    prob = Problem()

    comp = IndepVarComp()
    comp.add_output('x', val=np.random.random((num_nodes, 2)))
    prob.model.add_subsystem('ivc', comp, promotes=['*'])
                    
    comp = CosComp(num_nodes=num_nodes)
    prob.model.add_subsystem('cos_comp', comp, promotes=['*'])
    
    prob.setup()
                    
    prob.run_model()

    print(prob['x'])
    print(prob['y'])

    prob.check_partials(compact_print=True)
