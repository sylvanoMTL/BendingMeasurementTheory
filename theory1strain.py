import numpy as np

def calc_theory1_strain(F, x_F, x_b, L_b, D_o_s, D_i_s, h_b, e_b, E_s):
    """
    Calculate mechanical strains from Theory 1 (clamped cantilever).
    
    Parameters
    ----------
    F : float
        Applied force at handle [N]
    x_F : float
        Handle position [mm]
    x_b : float
        Beam root position [mm]
    L_b : float
        Beam length [mm]
    D_o_s : float
        Shaft outer diameter [mm]
    D_i_s : float
        Shaft inner diameter [mm]
    h_b : float
        Beam height (bending direction) [mm]
    e_b : float
        Beam eccentricity from shaft surface [mm]
    E_s : float
        Shaft Young's modulus [MPa]
    
    Returns
    -------
    dict
        Dictionary containing strains in microstrain (µε)
    """
    
    # Gauge position
    x_gauge = x_b + L_b / 2.0
    
    # Shaft second moment of area
    I_s = (np.pi / 64.0) * (D_o_s**4 - D_i_s**4)
    
    # Beam neutral axis position
    y_b = D_o_s / 2.0 + e_b
    
    # Top and bottom surface positions
    y_top = y_b + h_b / 2.0
    y_bottom = y_b - h_b / 2.0
    
    # Mechanical strains (dimensionless)
    eps_top = F * (x_F - x_gauge) * y_top / (E_s * I_s)
    eps_bottom = F * (x_F - x_gauge) * y_bottom / (E_s * I_s)
    delta_eps = F * (x_F - x_gauge) * h_b / (E_s * I_s)
    
    # Convert to microstrain
    return {
        'eps_top_ustrain': eps_top * 1e6,
        'eps_bottom_ustrain': eps_bottom * 1e6,
        'delta_eps_ustrain': delta_eps * 1e6,
        'eps_top': eps_top,
        'eps_bottom': eps_bottom,
        'delta_eps': delta_eps
    }


# Example usage with Concept2 parameters
if __name__ == "__main__":
    result = calc_theory1_strain(
        F=1962,        # Force [N]
        x_F=900,       # Handle position [mm]
        x_b=200,       # Beam root [mm]
        L_b=100,       # Beam length [mm]
        D_o_s=38,      # Shaft OD [mm]
        D_i_s=32,      # Shaft ID [mm]
        h_b=2,         # Beam height [mm]
        e_b=20,        # Beam eccentricity [mm]
        E_s=140e3      # Shaft modulus [MPa]
    )
    
    print("Theory 1 Mechanical Strains:")
    print(f"  Top surface:    {result['eps_top_ustrain']:.0f} µε")
    print(f"  Bottom surface: {result['eps_bottom_ustrain']:.0f} µε")
    print(f"  Differential:   {result['delta_eps_ustrain']:.0f} µε")