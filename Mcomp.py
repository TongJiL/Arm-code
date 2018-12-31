'''
from openmdao.api import Problem
import numpy as np
from openmdao.api import ExplicitComponent

class elements(ExplicitComponent):

    def initialize(self):
        self.options.declare('num', default=1, types=int)

    def setup(self):
        #inputs
        self.add_input('k',val=14.1543)
        self.add_input('E_k',val=0)
        self.add_input('tor',0.5)
        self.add_input('q',shape=(num,2))
        self.add_input('w',shape=(num,2))
        self.add_input('p_1')
        self.add_input('p_2')
        self.add_input('p_3')
        self.add_input('p_4')
        self.add_input('p_5')
        #outputs
        self.add_output('M_q',shape=(num,2,2))
        self.add_output('C_q',shape=(num,2,2))
        self.add_output('G_q',shape=(2,1,num))
        self.add_output('K_q',shape=(num,2))
        self.add_output('F',shape=(num,2))

        #partials
        self.declare_partials('M_q',['p_1','p_2','p_3','q'])
        self.declare_partials('C_q',['p_3','q','w'])
        self.declare_partials('G_q',['p_4','p_5','q'])
        self.declare_partials('K_q',['k','E_k','q'])
        self.declare_partials('F',['tor'])
            
    def compute(self,inputs,outputs):
    
        p_1=inputs['p_1']
        p_2=inputs['p_2']
        p_3=inputs['p_3']
        p_4=inputs['p_4']
        p_5=inputs['p_5']
        q_1=inputs['q'][:,0]
        q_2=inputs['q'][:,1]
        w_1=inputs['w'][:,0]
        w_2=inputs['w'][:,1]
        k=inputs['k']
        E_k=inputs['E_k']
        tor=inputs['tor']
        
        outputs['G_q']=list([[(p_4)*(np.cos(q_1))],[(p_5)*(np.cos(q_2))]])
        outputs['M_q']=list([[p_1,(p_3)*(np.cos(q_1-q_2))],
                                 [(p_3)*(np.cos(q_1-q_2)),p_2]])
        outputs['C_q']=list([[0,(p_3)*(np.sin(q_1-q_2))*w_2],
                                [-(p_3)*(np.sin(q_1-q_2))*w_1,0]])
        outputs['K_q']=list([[-k*(q_2-q_1-E_k)],
                                [(q_2-q_1-E_k)*k]])
        outputs['F']=list([[tor],[0]])
                              
    def compute_partials(self,inputs,J):
        
        p_1=inputs['p_1']
        p_2=inputs['p_2']
        p_3=inputs['p_3']
        p_4=inputs['p_4']
        p_5=inputs['p_5']
        q_1=inputs['q'][:,0]
        q_2=inputs['q'][:,1]
        w_1=inputs['w'][:,0]
        w_2=inputs['w'][:,1]
        k=inputs['k']
        E_k=inputs['E_k']
        tor=inputs['tor']
        
        J['M_q','p_1']=np.array([[1,0],[0,0]])
        J['M_q','p_2']=np.array([[0,0],[0,1]])
        J['M_q','p_3']=np.array([[0,cos(q_1-q_2)],[cos(q_1-q_2),0]])
        J['M_q','q_1']=np.array([[0,-sin(q_1-q_2)],[-sin(q_1-q_2),0]])
        J['M_q','q_2']=np.array([[0,sin(q_1-q_2)],[sin(q_1-q_2),0]])
        J['C_q','p_3']=np.array([[0,sin(q_1-q_2)*w_2],[-sin(q_1-q_2)*w_1,0]])
        J['C_q','q_1']=np.array([[0,p_3*cos(q_1-q_2)*w_2],[-p_3*cos(q_1-q_2)*w_1,0]])
        J['C_q','q_2']=np.array([[0,-p_3*cos(q_1-q_2)*w_2],[p_3*cos(q_1-q_2)*w_1,0]])
        J['C_q','w_1']=np.array([[0,0],[-p_3*sin(q_1-q_2),0]])
        J['C_q','w_2']=np.array([[0,p_3*sin(q_1-q_2)],[0,0]])
        J['G_q','p_4']=np.array([[cos(q_1)],[0]])
        J['G_q','p_5']=np.array([[0],[cos(q_2)]])
        J['G_q','q_1']=np.array([[-p_4*sin(q_1)],[0]])
        J['G_q','q_2']=np.array([[0],[-p_5*sin(q_2)]])
        J['K_q','k']=np.array([[q_1+E_k-q_2],[q_2-q_1-E_k]])
        J['K_q','E_k']=np.array([[k],[-k]])
        J['K_q','q_1']=np.array([[k],[-k]])
        J['K_q','q_2']=np.array([[-k],[k]])
        J['F','tor']=np.array([[1],[0]])



if __name__ == '__main__':
    from openmdao.api import Problem, IndepVarComp
    
    num = 20
    
    prob = Problem()
    
    comp = IndepVarComp()
    comp.add_output('k',val=14.1543)
    comp.add_output('E_k',val=0)
    comp.add_output('tor',0.5)
    comp.add_output('q',val=np.random.random((num,2)))
    comp.add_output('w',val=np.random.random((num,2)))
    comp.add_output('p_1',0.311658)
    comp.add_output('p_2',0.155)
    comp.add_output('p_3',0.10024)
    comp.add_output('p_4',9.39299)
    comp.add_output('p_5',3.278)
    prob.model.add_subsystem('ivc', comp, promotes=['*'])
    
    comp = elements(num=num)
    prob.model.add_subsystem('elements', comp, promotes=['*'])
    
    prob.setup()
    
    prob.run_model()
    
    print(prob['M_q'])
    print(prob['G_q'])
    print(prob['C_q'])
    print(prob['K_q'])
    print(prob['F'])
    
    prob.check_partials(compact_print=True)
'''
from openmdao.api import Problem
import numpy as np
from openmdao.api import ExplicitComponent

class elements(ExplicitComponent):
    
    def initialize(self):
        self.options.declare('num', default=1, types=int)
    
    def setup(self):
        #inputs
        self.add_input('k',val=14.1543)
        self.add_input('E_k',val=0)
        self.add_input('tor',0.5)
        self.add_input('q',shape=(num,2))
        self.add_input('w',shape=(num,2))
        self.add_input('p_1')
        self.add_input('p_2')
        self.add_input('p_3')
        self.add_input('p_4')
        self.add_input('p_5')
        #outputs
        self.add_output('M_q',shape=(num,2,2))
        self.add_output('C_q',shape=(num,2,2))
        self.add_output('G_q',shape=(num,2,1))
        self.add_output('K_q',shape=(num,2,1))
        self.add_output('F',shape=(2,1))
        
        #partials
        self.declare_partials('M_q',['p_1','p_2','p_3','q'])
        self.declare_partials('C_q',['p_3','q','w'])
        self.declare_partials('G_q',['p_4','p_5','q'])
        self.declare_partials('K_q',['k','E_k','q'])
        self.declare_partials('F',['tor'])
    
    def compute(self,inputs,outputs):
        
        p_1=inputs['p_1']
        p_2=inputs['p_2']
        p_3=inputs['p_3']
        p_4=inputs['p_4']
        p_5=inputs['p_5']
        for i in range(20):
            q_1=inputs['q'][i,0]
            q_2=inputs['q'][i,1]
            w_1=inputs['w'][i,0]
            w_2=inputs['w'][i,1]
            k=inputs['k']
            E_k=inputs['E_k']
            tor=inputs['tor']
            
            
            outputs['M_q'][i,:,:]=list([[p_1,(p_3)*(np.cos(q_1-q_2))],[(p_3)*(np.cos(q_1-q_2)),p_2]])
            outputs['C_q'][i,:,:]=list([[0,(p_3)*(np.sin(q_1-q_2))*w_2],
                                        [-(p_3)*(np.sin(q_1-q_2))*w_1,0]])
            outputs['K_q'][i,:,:]=list([[-k*(q_2-q_1-E_k)],[(q_2-q_1-E_k)*k]])
            outputs['G_q'][i,:,:]=list([[(p_4)*(np.cos(q_1))],[(p_5)*(np.cos(q_2))]])
        
        outputs['F']=list([[tor],[0]])
    
    def compute_partials(self,inputs,J):
        
        p_1=inputs['p_1']
        p_2=inputs['p_2']
        p_3=inputs['p_3']
        p_4=inputs['p_4']
        p_5=inputs['p_5']
        q_1=inputs['q'][:,0]
        q_2=inputs['q'][:,1]
        w_1=inputs['w'][:,0]
        w_2=inputs['w'][:,1]
        k=inputs['k']
        E_k=inputs['E_k']
        tor=inputs['tor']
        
        J['M_q','p_1']=np.array([[1,0],[0,0]])
        J['M_q','p_2']=np.array([[0,0],[0,1]])
        J['M_q','p_3']=np.array([[0,np.cos(q_1-q_2)],[np.cos(q_1-q_2),0]])
        J['M_q','q_1']=np.array([[0,-np.sin(q_1-q_2)],[-np.sin(q_1-q_2),0]])
        J['M_q','q_2']=np.array([[0,np.sin(q_1-q_2)],[np.sin(q_1-q_2),0]])
        J['C_q','p_3']=np.array([[0,np.sin(q_1-q_2)*w_2],[-np.sin(q_1-q_2)*w_1,0]])
        J['C_q','q_1']=np.array([[0,p_3*np.cos(q_1-q_2)*w_2],[-p_3*np.cos(q_1-q_2)*w_1,0]])
        J['C_q','q_2']=np.array([[0,-p_3*np.cos(q_1-q_2)*w_2],[p_3*np.cos(q_1-q_2)*w_1,0]])
        J['C_q','w_1']=np.array([[0,0],[-p_3*np.sin(q_1-q_2),0]])
        J['C_q','w_2']=np.array([[0,p_3*np.sin(q_1-q_2)],[0,0]])
        J['G_q','p_4']=np.array([[np.cos(q_1)],[0]])
        J['G_q','p_5']=np.array([[0],[np.cos(q_2)]])
        J['G_q','q_1']=np.array([[-p_4*np.sin(q_1)],[0]])
        J['G_q','q_2']=np.array([[0],[-p_5*np.sin(q_2)]])
        J['K_q','k']=[[q_1+E_k-q_2],[q_2-q_1-E_k]]
        J['K_q','E_k']=[[k],[-k]]
        J['K_q','q_1']=[[k],[-k]]
        J['K_q','q_2']=[[-k],[k]]
        J['F','tor']=[[1],[0]]



if __name__ == '__main__':
    from openmdao.api import Problem, IndepVarComp
    
    num = 20
    
    prob = Problem()
    
    comp = IndepVarComp()
    comp.add_output('k',val=14.1543)
    comp.add_output('E_k',val=0)
    comp.add_output('tor',0.5)
    comp.add_output('q',val=np.random.random((num,2)))
    comp.add_output('w',val=np.random.random((num,2)))
    comp.add_output('p_1',0.311658)
    comp.add_output('p_2',0.155)
    comp.add_output('p_3',0.10024)
    comp.add_output('p_4',9.39299)
    comp.add_output('p_5',3.278)
    prob.model.add_subsystem('ivc', comp, promotes=['*'])
    
    comp = elements(num=num)
    prob.model.add_subsystem('elements', comp, promotes=['*'])
    
    prob.setup()
    
    prob.run_model()
    
    print(prob['M_q'])
    print(prob['G_q'])
    print(prob['C_q'])
    print(prob['K_q'])
    print(prob['F'])
    
    prob.check_partials(compact_print=True)
