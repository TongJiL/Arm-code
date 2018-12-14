from openmdao.api import ExplicitComponent
import math
import numpy as np



class dcomp(ExplicitComponent):

    def initialize(self):
        self.options.declare('num', default=1, types=int)


    def setup(self):
        #input
        self.add_input('x')
        self.add_input('y')
        self.add_input('dotx')
        self.add_input('doty')

        #output
        self.add_output('d')

        #partials
        self.declare_partials('dotx',['x','y','dotx','doty'])

    def compute(self,inputs,outputs):

        x=inputs['x']
        y=inputs['y']
        dotx=inputs['dotx']
        doty=inputs['doty']

        outputs['d']=dotx*doty/9.81+np.sqrt((dotx*doty/9.81)**2+(2*dotx**2*y/9.81))+x

    def compute_partials(self,inputs,J):

        x=inputs['x']
        y=inputs['y']
        dotx=inputs['dotx']
        doty=inputs['doty']


        J['d','x']=1
        J['d','y']=dotx**2/(9.81*np.sqrt((dotx*doty/9.81)**2+(2*dotx**2*y/9.81)))
        J['d','dotx']=doty/9.81+(dotx*doty**2/9.81+2*dotx*y)/(9.81*np.sqrt((dotx*doty/9.81)**2+(2*dotx**2*y/9.81)))
        J['d','doty']=dotx/9.81+(dotx**2*doty)/(9.81**2*np.sqrt((dotx*doty/9.81)**2+(2*dotx**2*y/9.81)))

if __name__ == '__main__':
    from openmdao.api import Problem, IndepVarComp
    
    num = 20
    
    prob = Problem()
    
    comp = IndepVarComp()
    comp.add_output('x',val=np.random)
    comp.add_output('y',val=np.random)
    comp.add_output('dotx',val=np.random)
    comp.add_output('doty',val=np.random)



    prob.model.add_subsystem('ivc', comp, promotes=['*'])
    
    comp = dcomp(num=num)
    prob.model.add_subsystem('dcomp', comp, promotes=['*'])
    
    prob.setup()
    
    prob.run_model()
    
    print(prob['d'])
    
    prob.check_partials(compact_print=True)

