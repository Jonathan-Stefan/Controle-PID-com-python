import control as ctrl

def Pid (Kp, Ti, Td):
    num_pid = [Kp * Td, Kp, Kp / Ti]
    den_pid = [1, 0]
    pid = ctrl.TransferFunction(num_pid, den_pid)

    return pid

def CHR20 (theta, tau, k):
    Kp = 0.95 * tau / (k * theta)
    Ti = 1.357 * tau
    Td = 0.4730 * theta
    return Kp, Ti, Td

def CohenCoon (theta, tau, k):
    Kp = (1.35 + 0.25 * (theta / tau)) * tau / (k * theta)
    Ti = (1.35 + 0.25 * (theta/tau)) / (0.54 + 0.33 * (theta / tau)) * theta
    Td = 0.5 * theta / (1.35 + 0.25*(theta/tau))
    
    return Kp, Ti, Td