"""
Rowing Oar Strain Calculator - Theory 1
Based on clamped cantilever beam model
Author: Sylvain Boyer (Mecafrog.com)
"""

import numpy as np

class OarStrainCalculator:
    """Calculator for mechanical strains in rowing oar measurement system."""
    
    def __init__(self):
        """Initialize with default Concept2 sculling oar parameters."""
        
        # Oar geometry [mm]
        self.x_F = 900.0          # Handle position
        self.x_b = 200.0          # Beam root position
        self.L_b = 100.0          # Beam length
        
        # Shaft geometry [mm]
        self.D_o_s = 38.0         # Shaft outer diameter
        self.D_i_s = 32.0         # Shaft inner diameter
        
        # Beam geometry [mm]
        self.h_b = 2.0            # Beam height (bending direction)
        self.b = 12.0             # Beam width
        self.e_b = 20.0           # Beam eccentricity from shaft surface
        
        # Material properties
        self.E_s = 140e3          # Shaft Young's modulus [MPa]
        self.E_b = 69e3           # Beam Young's modulus [MPa]
        
        # Strain gauge parameters
        self.GF = 2.15            # Gauge factor
        self.V_ex = 3.3           # Bridge excitation voltage [V]
        
        # Applied force [N]
        self.F = 1962.0           # Peak force (200 kg)
    
    def calc_shaft_inertia(self):
        """Calculate shaft second moment of area [mm^4]."""
        D_o = self.D_o_s
        D_i = self.D_i_s
        return (np.pi / 64.0) * (D_o**4 - D_i**4)
    
    def calc_beam_inertia(self):
        """Calculate beam second moment of area [mm^4]."""
        return (self.b * self.h_b**3) / 12.0
    
    def calc_gauge_position(self):
        """Calculate gauge x-position [mm]."""
        return self.x_b + self.L_b / 2.0
    
    def calc_gauge_radii(self):
        """Calculate gauge y-positions from shaft centerline [mm]."""
        y_b = self.D_o_s / 2.0 + self.e_b
        y_top = y_b + self.h_b / 2.0
        y_bottom = y_b - self.h_b / 2.0
        return y_b, y_top, y_bottom
    
    def calc_curvature(self, x):
        """Calculate shaft curvature at position x [1/mm]."""
        I_s = self.calc_shaft_inertia()
        return self.F * (self.x_F - x) / (self.E_s * I_s)
    
    def calc_strains(self):
        """Calculate mechanical strains at gauge locations."""
        # Geometry
        x_gauge = self.calc_gauge_position()
        y_b, y_top, y_bottom = self.calc_gauge_radii()
        
        # Curvature at gauge
        kappa = self.calc_curvature(x_gauge)
        
        # Mechanical strains
        eps_top = kappa * y_top
        eps_bottom = kappa * y_bottom
        delta_eps = eps_top - eps_bottom
        
        return {
            'x_gauge': x_gauge,
            'y_b': y_b,
            'y_top': y_top,
            'y_bottom': y_bottom,
            'curvature': kappa,
            'eps_top': eps_top,
            'eps_bottom': eps_bottom,
            'delta_eps': delta_eps,
            'eps_top_ustrain': eps_top * 1e6,
            'eps_bottom_ustrain': eps_bottom * 1e6,
            'delta_eps_ustrain': delta_eps * 1e6
        }
    
    def calc_bridge_output(self):
        """Calculate normalized bridge output voltage."""
        results = self.calc_strains()
        delta_eps = results['delta_eps']
        return (self.GF / 2.0) * delta_eps
    
    def print_results(self):
        """Print calculation results in readable format."""
        print("=" * 60)
        print("ROWING OAR STRAIN CALCULATOR - THEORY 1")
        print("=" * 60)
        
        print("\nInput Parameters:")
        print(f"  Applied Force:           F = {self.F:.1f} N")
        print(f"  Handle Position:      x_F = {self.x_F:.1f} mm")
        print(f"  Beam Root:            x_b = {self.x_b:.1f} mm")
        print(f"  Beam Length:          L_b = {self.L_b:.1f} mm")
        print(f"  Shaft OD:           D_o_s = {self.D_o_s:.1f} mm")
        print(f"  Shaft ID:           D_i_s = {self.D_i_s:.1f} mm")
        print(f"  Beam Height:          h_b = {self.h_b:.1f} mm")
        print(f"  Beam Eccentricity:    e_b = {self.e_b:.1f} mm")
        print(f"  Shaft Modulus:        E_s = {self.E_s/1e3:.0f} GPa")
        
        I_s = self.calc_shaft_inertia()
        I_b = self.calc_beam_inertia()
        print(f"\nCalculated Properties:")
        print(f"  Shaft Inertia:        I_s = {I_s:.0f} mm^4")
        print(f"  Beam Inertia:         I_b = {I_b:.2f} mm^4")
        
        results = self.calc_strains()
        print(f"\nGauge Geometry:")
        print(f"  Gauge Position:    x_gauge = {results['x_gauge']:.1f} mm")
        print(f"  Beam Neutral Axis:    y_b = {results['y_b']:.1f} mm")
        print(f"  Top Surface:        y_top = {results['y_top']:.1f} mm")
        print(f"  Bottom Surface:  y_bottom = {results['y_bottom']:.1f} mm")
        
        print(f"\nMechanical Strains:")
        print(f"  Curvature:          kappa = {results['curvature']*1e3:.3f} m^-1")
        print(f"  Top Strain:       eps_top = {results['eps_top_ustrain']:.0f} µε")
        print(f"  Bottom Strain: eps_bottom = {results['eps_bottom_ustrain']:.0f} µε")
        print(f"  Differential:   delta_eps = {results['delta_eps_ustrain']:.0f} µε")
        
        V_ratio = self.calc_bridge_output()
        V_out = V_ratio * self.V_ex * 1e3  # Convert to mV
        print(f"\nBridge Output:")
        print(f"  Normalized:     V_out/V_ex = {V_ratio*1e3:.3f} mV/V")
        print(f"  Output Voltage:      V_out = {V_out:.3f} mV")
        print(f"                              = {V_out*1e3:.0f} µV")
        
        print("=" * 60)


def parametric_study_force():
    """Example: Parametric study varying applied force."""
    print("\nPARAMETRIC STUDY: Strain vs Force")
    print("-" * 60)
    
    calc = OarStrainCalculator()
    forces = np.array([0, 500, 1000, 1500, 1962, 2500])
    
    print(f"{'Force [N]':>10} {'eps_top [µε]':>15} {'delta_eps [µε]':>15} {'V_out [mV]':>12}")
    print("-" * 60)
    
    for F in forces:
        calc.F = F
        results = calc.calc_strains()
        V_out = calc.calc_bridge_output() * calc.V_ex * 1e3
        
        print(f"{F:10.0f} {results['eps_top_ustrain']:15.0f} "
              f"{results['delta_eps_ustrain']:15.0f} {V_out:12.3f}")


def parametric_study_geometry():
    """Example: Parametric study varying beam height."""
    print("\nPARAMETRIC STUDY: Strain vs Beam Height")
    print("-" * 60)
    
    calc = OarStrainCalculator()
    heights = np.array([1.0, 1.5, 2.0, 2.5, 3.0])
    
    print(f"{'h_b [mm]':>10} {'delta_eps [µε]':>15} {'V_out [mV]':>12}")
    print("-" * 60)
    
    for h in heights:
        calc.h_b = h
        results = calc.calc_strains()
        V_out = calc.calc_bridge_output() * calc.V_ex * 1e3
        
        print(f"{h:10.1f} {results['delta_eps_ustrain']:15.0f} {V_out:12.3f}")


if __name__ == "__main__":
    # Basic calculation with default parameters
    calc = OarStrainCalculator()
    calc.print_results()
    
    # Parametric studies
    parametric_study_force()
    parametric_study_geometry()