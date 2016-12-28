from gpkit import Variable, Model, ureg
from shopping import ShoppingCart

# Just a copy of opt.py
def test():
     # Configuration
     n_rotors = Variable('n_rotors', 4, '-')
     payload_mass = Variable('payload_mass', 0.1, 'kg')
     structures_mass = Variable('structures_mass', 0.2, 'kg')

     # Battery
     battery_mass = Variable('battery_mass', 'kg')
     battery_energy = Variable('battery_energy', 'J')
     battery_shopping = ShoppingCart(goods={battery_energy: [200, 7.53, 533]*ureg.kJ},
                                     bads={battery_mass: [1.189, 0.119, 0.804]*ureg.kg})

     # ESC
     esc_mass = Variable('esc_mass', 'kg')
     esc_power = Variable('esc_power', 'W')
     esc_specificPower = Variable('esc_specificPower', 500, 'W/kg')

     # Motor
     motor_mass = Variable('motor_mass', 'kg')
     motor_power = Variable('motor_power', 'W')
     motor_shopping = ShoppingCart(goods={motor_power: [49, 194.3, 59.2, 384.1]*ureg.W},
                                   bads={motor_mass: [16., 127, 13, 162]*ureg.grams})
     # print type([49, 194.3, 59.2, 384.1])
     # Propeller
     propeller_d = Variable('propeller_d', 0.1, 'm')
     propeller_efficiency = Variable('propeller_efficiency', 0.9, '-')

     # Performance variables
     t_hover = Variable('t_hover', 's')
     T_total = Variable('T_total', 'N')
     P_total = Variable('P_total', 'W')
     m_total = Variable('m_total', 'kg')

     # Environment
     rho = Variable('rho', 1.225, 'kg/m^3')
     g = Variable('g', 9.8, 'm/s/s')

     # Constraints
     constraints = [battery_shopping,
                    esc_power <= esc_specificPower*esc_mass,
                    motor_shopping,
                    esc_power >= motor_power,
                    T_total <= 3.141/2 * rho*ureg('m^3/kg') * (propeller_efficiency*n_rotors*motor_power**(0.6)*propeller_d**(0.6)*ureg('(N/(W^0.6 * m^0.6))')),
                    m_total >= n_rotors*(esc_mass+motor_mass) + battery_mass+payload_mass+structures_mass,
                    P_total >= n_rotors*esc_power,
                    T_total >= m_total*g,
                    t_hover <= battery_energy/P_total,
                    t_hover >= Variable('t_hoverLimit', 120, 's')]

     # Objective (to minimize)
     # objective = 1/t_hover
     objective = (1/t_hover)**0.0001 * ((m_total*g)/T_total)**5

     # Formulate the Model
     m = Model(objective, constraints)
     # m.debug()
     # Solve the Model
     sol = m.solve(verbosity=1)

if __name__ == '__main__':
    test()