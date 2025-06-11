import time
import random
import math
import statistics

def generate_3d_test_data(num_points):
    """Generate random 3D coordinates and target point"""
    sources = [(random.uniform(0, 1000), random.uniform(0, 1000), random.uniform(0, 1000)) 
               for _ in range(num_points)]
    target = (500, 500, 500)
    return sources, target

def find_closest_3d_with_sqrt(sources, target):
    """Find closest 3D point using sqrt (actual distance)"""
    min_dist = float('inf')
    closest_point = None
    for x, y, z in sources:
        dx = x - target[0]
        dy = y - target[1]
        dz = z - target[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < min_dist:
            min_dist = dist
            closest_point = (x, y, z)
    return closest_point, min_dist

def find_closest_3d_with_squared(sources, target):
    """Find closest 3D point using squared distance (no sqrt)"""
    min_dist_sq = float('inf')
    closest_point = None
    for x, y, z in sources:
        dx = x - target[0]
        dy = y - target[1]
        dz = z - target[2]
        dist_sq = dx*dx + dy*dy + dz*dz
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            closest_point = (x, y, z)
    return closest_point, min_dist_sq

def find_closest_3d_with_manhattan(sources, target):
    """Find closest 3D point using Manhattan distance (sum of absolute differences)"""
    min_dist = float('inf')
    closest_point = None
    for x, y, z in sources:
        dist = abs(x - target[0]) + abs(y - target[1]) + abs(z - target[2])
        if dist < min_dist:
            min_dist = dist
            closest_point = (x, y, z)
    return closest_point, min_dist

def benchmark_3d_method(method_func, sources, target, num_runs=15):
    """Benchmark a 3D method multiple times and return statistics"""
    times = []
    results = []
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        result = method_func(sources, target)
        end_time = time.perf_counter()
        
        times.append(end_time - start_time)
        results.append(result)
    
    return {
        'times': times,
        'mean_time': statistics.mean(times),
        'median_time': statistics.median(times),
        'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
        'min_time': min(times),
        'max_time': max(times),
        'results': results
    }

def run_3d_benchmark():
    """Run comprehensive 3D distance benchmark"""
    
    # Test with different dataset sizes
    dataset_sizes = [10000, 50000, 100000, 500000]
    num_runs = 15
    
    print("=== 3D Distance Calculation Benchmark ===")
    print(f"Number of runs per test: {num_runs}")
    print(f"Comparing: Euclidean (sqrt), Squared Euclidean, Manhattan distances")
    print()
    
    for num_points in dataset_sizes:
        print(f"--- Testing with {num_points:,} 3D points ---")
        
        # Generate test data once for consistency
        sources, target = generate_3d_test_data(num_points)
        
        # Benchmark all three methods
        sqrt_stats = benchmark_3d_method(find_closest_3d_with_sqrt, sources, target, num_runs)
        squared_stats = benchmark_3d_method(find_closest_3d_with_squared, sources, target, num_runs)
        manhattan_stats = benchmark_3d_method(find_closest_3d_with_manhattan, sources, target, num_runs)
        
        # Verify Euclidean methods find the same point
        sqrt_point = sqrt_stats['results'][0][0]
        squared_point = squared_stats['results'][0][0]
        manhattan_point = manhattan_stats['results'][0][0]
        
        euclidean_match = sqrt_point == squared_point
        
        # Calculate performance ratios
        sqrt_vs_squared = sqrt_stats['mean_time'] / squared_stats['mean_time']
        sqrt_vs_manhattan = sqrt_stats['mean_time'] / manhattan_stats['mean_time']
        squared_vs_manhattan = squared_stats['mean_time'] / manhattan_stats['mean_time']
        
        # Display results
        print(f"  Euclidean methods find same point: {euclidean_match}")
        print(f"  Manhattan finds different point: {sqrt_point != manhattan_point} (expected)")
        print()
        
        print(f"  EUCLIDEAN (sqrt) method:")
        print(f"    Mean time: {sqrt_stats['mean_time']:.6f}s")
        print(f"    Std dev: {sqrt_stats['std_dev']:.6f}s")
        
        print(f"  SQUARED EUCLIDEAN method:")
        print(f"    Mean time: {squared_stats['mean_time']:.6f}s")
        print(f"    Std dev: {squared_stats['std_dev']:.6f}s")
        
        print(f"  MANHATTAN method:")
        print(f"    Mean time: {manhattan_stats['mean_time']:.6f}s")
        print(f"    Std dev: {manhattan_stats['std_dev']:.6f}s")
        
        print(f"  Performance Comparisons:")
        if sqrt_vs_squared > 1:
            print(f"    SQUARED is {sqrt_vs_squared:.2f}x FASTER than SQRT")
        else:
            print(f"    SQRT is {1/sqrt_vs_squared:.2f}x FASTER than SQUARED")
            
        if sqrt_vs_manhattan > 1:
            print(f"    MANHATTAN is {sqrt_vs_manhattan:.2f}x FASTER than SQRT")
        else:
            print(f"    SQRT is {1/sqrt_vs_manhattan:.2f}x FASTER than MANHATTAN")
            
        if squared_vs_manhattan > 1:
            print(f"    MANHATTAN is {squared_vs_manhattan:.2f}x FASTER than SQUARED")
        else:
            print(f"    SQUARED is {1/squared_vs_manhattan:.2f}x FASTER than MANHATTAN")
        
        print(f"    Ratios - sqrt/squared: {sqrt_vs_squared:.4f}, sqrt/manhattan: {sqrt_vs_manhattan:.4f}")
        print()

def compare_distance_metrics():
    """Compare different distance metrics with a small example"""
    print("=== Distance Metric Comparison (Small Example) ===")
    
    # Create a simple test case
    point1 = (0, 0, 0)
    point2 = (3, 4, 5)
    
    # Calculate different distances
    dx, dy, dz = point2[0] - point1[0], point2[1] - point1[1], point2[2] - point1[2]
    
    euclidean = math.sqrt(dx*dx + dy*dy + dz*dz)
    squared_euclidean = dx*dx + dy*dy + dz*dz
    manhattan = abs(dx) + abs(dy) + abs(dz)
    
    print(f"Point 1: {point1}")
    print(f"Point 2: {point2}")
    print(f"Euclidean distance: {euclidean:.4f}")
    print(f"Squared Euclidean distance: {squared_euclidean:.4f}")
    print(f"Manhattan distance: {manhattan:.4f}")
    print()

# Warm up Python interpreter
print("Warming up 3D calculations...")
sources, target = generate_3d_test_data(1000)
for _ in range(3):
    find_closest_3d_with_sqrt(sources, target)
    find_closest_3d_with_squared(sources, target)
    find_closest_3d_with_manhattan(sources, target)

# Show distance metric comparison first
compare_distance_metrics()

# Run the comprehensive benchmark
run_3d_benchmark()

# Additional analysis: Memory and computational complexity
print("=== Computational Complexity Analysis ===")
print("Per point calculations:")
print("  SQRT: 3 subtractions + 3 multiplications + 2 additions + 1 sqrt = ~7 ops + sqrt")
print("  SQUARED: 3 subtractions + 3 multiplications + 2 additions = ~8 simple ops")
print("  MANHATTAN: 3 subtractions + 3 absolute values + 2 additions = ~8 simple ops")
print()
print("Note: sqrt is typically 10-20x more expensive than basic arithmetic operations")
print("3D vs 2D: Additional dimension adds ~33% more arithmetic operations")
