import time
import random
import math
import statistics

def generate_test_data(num_points):
    """Generate random coordinates and target point"""
    sources = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(num_points)]
    target = (500, 500)
    return sources, target

def find_closest_with_sqrt(sources, target):
    """Find closest point using sqrt (actual distance)"""
    min_dist = float('inf')
    closest_point = None
    for x, y in sources:
        dx = x - target[0]
        dy = y - target[1]
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < min_dist:
            min_dist = dist
            closest_point = (x, y)
    return closest_point, min_dist

def find_closest_with_squared(sources, target):
    """Find closest point using squared distance (no sqrt)"""
    min_dist_sq = float('inf')
    closest_point = None
    for x, y in sources:
        dx = x - target[0]
        dy = y - target[1]
        dist_sq = dx * dx + dy * dy
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            closest_point = (x, y)
    return closest_point, min_dist_sq

def benchmark_method(method_func, sources, target, num_runs=10):
    """Benchmark a method multiple times and return statistics"""
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

def run_comprehensive_benchmark():
    """Run comprehensive benchmark with multiple configurations"""
    
    # Test with different dataset sizes
    dataset_sizes = [10000, 50000, 100000, 500000]
    num_runs = 20  # Number of runs per test
    
    print("=== Distance Calculation Benchmark ===")
    print(f"Number of runs per test: {num_runs}")
    print(f"Using time.perf_counter() for higher precision")
    print()
    
    for num_points in dataset_sizes:
        print(f"--- Testing with {num_points:,} points ---")
        
        # Generate test data once for consistency
        sources, target = generate_test_data(num_points)
        
        # Benchmark sqrt method
        sqrt_stats = benchmark_method(find_closest_with_sqrt, sources, target, num_runs)
        
        # Benchmark squared method  
        squared_stats = benchmark_method(find_closest_with_squared, sources, target, num_runs)
        
        # Verify both methods find the same point
        sqrt_point = sqrt_stats['results'][0][0]
        squared_point = squared_stats['results'][0][0]
        points_match = sqrt_point == squared_point
        
        # Calculate performance ratio
        speed_ratio = sqrt_stats['mean_time'] / squared_stats['mean_time']
        
        # Display results
        print(f"  Points match: {points_match}")
        print(f"  SQRT method:")
        print(f"    Mean time: {sqrt_stats['mean_time']:.6f}s")
        print(f"    Median time: {sqrt_stats['median_time']:.6f}s") 
        print(f"    Std dev: {sqrt_stats['std_dev']:.6f}s")
        print(f"    Range: {sqrt_stats['min_time']:.6f}s - {sqrt_stats['max_time']:.6f}s")
        
        print(f"  SQUARED method:")
        print(f"    Mean time: {squared_stats['mean_time']:.6f}s")
        print(f"    Median time: {squared_stats['median_time']:.6f}s")
        print(f"    Std dev: {squared_stats['std_dev']:.6f}s")
        print(f"    Range: {squared_stats['min_time']:.6f}s - {squared_stats['max_time']:.6f}s")
        
        print(f"  Performance:")
        if speed_ratio > 1:
            print(f"    SQUARED is {speed_ratio:.2f}x FASTER than SQRT")
        else:
            print(f"    SQRT is {1/speed_ratio:.2f}x FASTER than SQUARED")
        
        print(f"    Speed ratio (sqrt/squared): {speed_ratio:.4f}")
        print()

# Warm up Python interpreter
print("Warming up...")
sources, target = generate_test_data(1000)
for _ in range(5):
    find_closest_with_sqrt(sources, target)
    find_closest_with_squared(sources, target)

# Run the comprehensive benchmark
run_comprehensive_benchmark()

# Quick single test for comparison with original
print("=== Quick Single Test (similar to original) ===")
sources, target = generate_test_data(10000)

start_sqrt = time.perf_counter()
closest_sqrt, _ = find_closest_with_sqrt(sources, target)
time_sqrt = time.perf_counter() - start_sqrt

start_sq = time.perf_counter()
closest_sq, _ = find_closest_with_squared(sources, target)
time_sq = time.perf_counter() - start_sq

print(f"Single run results:")
print(f"Points match: {closest_sqrt == closest_sq}")
print(f"SQRT time: {time_sqrt:.6f}s")
print(f"SQUARED time: {time_sq:.6f}s") 
print(f"Ratio (sqrt/squared): {time_sqrt/time_sq:.4f}")
