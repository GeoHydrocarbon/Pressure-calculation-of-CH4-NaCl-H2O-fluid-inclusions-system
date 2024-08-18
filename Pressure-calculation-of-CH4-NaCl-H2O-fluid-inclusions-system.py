import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 设置WebDriver的路径，根据你下载的WebDriver的实际路径进行设置
wd = webdriver.Chrome()

F = 0.032   #设置气泡大小
print('F:', F)

#ρ1的计算
M_H2O = 0.0180148       #kg/mol
M_CH4 = 0.016042        #kg/mol
M_NaCl = 0.0584428         #：MNaCl 为 NaCl 的 分 子 量(Kg/mol)
D = -2.35
ice_t = -15.6
S = (0-1.78*ice_t-0.0442 *ice_t*ice_t-0.000557 *ice_t*ice_t*ice_t)/100
m_NaCl = S/(M_NaCl*(1-S))       #NaCl 的质量摩尔浓度 mNaCl
m_NaCl = round(m_NaCl, 3)      #mol/kg
print('m_NaCl', m_NaCl)
T_n = 22 + 273.15
T_h = 154.5 + 273.15
P_l = (-0.0148*(D**5)-0.1791*(D**4)-0.8479*(D**3)-1.765*(D**2)-5.876*D)*10  #计算常温下的压力
P_l = round(P_l, 5)
print('P_l:', P_l)


def density_CH4_gas(P_l, T_n):
    wd.get('http://159.226.119.204:8080/models/ch4/calc.php')
    element_T_n = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]')
    element_T_n.send_keys(T_n)

    element_P_n = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(3) > td:nth-child(2) > input[type=text]')
    element_P_n.send_keys(P_l)

    element_calculate3 = wd.find_element(By.CSS_SELECTOR, 'body > form > input[type=submit]:nth-child(2)')
    element_calculate3.click()

    time.sleep(1)

    #g/cm3 室温下富水溶液包裹体中的气相密度ρ气泡
    element_den_g = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(7) > td:nth-child(2) > font')
    den_g = float(element_den_g.get_attribute('textContent'))   #g/cm3
    den_g = den_g     #g/cm3
    den_g = round(den_g, 5)
    print('den_g:', den_g)
    return den_g

den_g = density_CH4_gas(P_l, T_n)


# 打开网页
def Solubility_Calculations(T_n, P_l, m_NaCl):
    wd.get('http://159.226.119.204:8080/models/h2o_ch4_nacl/hle/calc.php')

    element_T_n = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]')
    element_T_n.send_keys(T_n)

    element_P_n = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=text]')
    element_P_n.send_keys(P_l)

    element_m_NaCl = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(5) > td:nth-child(2) > input[type=text]')
    element_m_NaCl.send_keys(m_NaCl)

    element_calculate1 = wd.find_element(By.CSS_SELECTOR, 'body > form > input[type=submit]:nth-child(3)')
    element_calculate1.click()

    time.sleep(1)

    element_m_CH4_output = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(9) > td:nth-child(2)')
    m_CH4 = float(element_m_CH4_output.get_attribute('textContent'))    #mol/kg
    m_CH4 = round(m_CH4, 5)
    print('m_CH4:', m_CH4)

    return m_CH4

m_CH4 = Solubility_Calculations(T_n, P_l, m_NaCl)


def Den_liquid_Normal (T_n, m_NaCl, m_CH4):
    wd.get('http://159.226.119.204:8080/models/h2o_ch4_nacl/homo/calc.php')

    element_T_n = wd.find_element(By.CSS_SELECTOR,
                                  '#table1 > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]')
    element_T_n.send_keys(T_n)

    element_m_NaCl = wd.find_element(By.CSS_SELECTOR,
                                  '#table1 > tbody > tr:nth-child(3) > td:nth-child(2) > input[type=text]')
    element_m_NaCl.send_keys(m_NaCl)

    element_m_CH4 = wd.find_element(By.CSS_SELECTOR,
                                     '#table1 > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=text]')
    element_m_CH4.send_keys(m_CH4)

    element_calculate1 = wd.find_element(By.CSS_SELECTOR, 'body > form:nth-child(3) > input[type=submit]:nth-child(4)')
    element_calculate1.click()

    time.sleep(1)

    element_den_liquid_output = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(8) > td:nth-child(2)')
    den_liquid_normal = float(element_den_liquid_output.get_attribute('textContent'))  # g/cm3
    den_liquid_normal = round(den_liquid_normal, 5)
    print('den_liquid_normal:', den_liquid_normal)
    return den_liquid_normal

den_liquid_normal = Den_liquid_Normal(T_n, m_NaCl,m_CH4)


den1 = den_g * F + den_liquid_normal * (1-F)            #求得包裹体的总密度 ρ总1  g/cm3
# den1 = den1*10**3
print('den1：', den1)

#ρ2的计算
b_CH4 = (m_CH4*den_liquid_normal*(1-F)+den_g*F/M_CH4)/(den_liquid_normal*(1-F)-den_liquid_normal*(1-F)*m_NaCl*M_NaCl-den_liquid_normal*(1-F)*m_CH4*M_CH4)
b_CH4 = round(b_CH4, 5)
print('b_CH4:', b_CH4)

def den2_and_P_h (T_h, m_NaCl, b_CH4):
    wd.get('http://159.226.119.204:8080/models/h2o_ch4_nacl/homo/calc.php')

    element_T_h = wd.find_element(By.CSS_SELECTOR,
                                  '#table1 > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]')
    element_T_h.send_keys(T_h)

    element_m_NaCl = wd.find_element(By.CSS_SELECTOR,
                                  '#table1 > tbody > tr:nth-child(3) > td:nth-child(2) > input[type=text]')
    element_m_NaCl.send_keys(m_NaCl)

    element_b_CH4 = wd.find_element(By.CSS_SELECTOR,
                                     '#table1 > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=text]')
    element_b_CH4.send_keys(b_CH4)

    element_calculate1 = wd.find_element(By.CSS_SELECTOR, 'body > form:nth-child(3) > input[type=submit]:nth-child(4)')
    element_calculate1.click()

    time.sleep(1)

    element_den2_output = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(8) > td:nth-child(2)')
    den2 = float(element_den2_output.get_attribute('textContent'))  # mol/kg
    den2 = round(den2, 5)
    print('den_den2:', den2)

    element_P_h_output = wd.find_element(By.CSS_SELECTOR, '#table1 > tbody > tr:nth-child(7) > td:nth-child(2)')
    P_h = float(element_P_h_output.get_attribute('textContent'))  # mol/kg
    P_h = round(P_h, 3)
    print('P_h:', P_h)
    return den2, P_h

den2, P_h = den2_and_P_h(T_h, m_NaCl,b_CH4)

Distance_F = abs(den1-den2)
print('Distance_F:', Distance_F)
