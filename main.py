# Alexander Johansson, Matti Al hanota, Abdihakim Mahamed, Hamed Sarvari, Elias Dovkrans

import functions


if __name__ == "__main__":
    n = 40
    print(f"=== Testing n = {n} ===")
    
    results_normal = [functions.fit(n, child_count=20, mutation_prob=0.1, generations=5000) for _ in range(5)]
    succ_normal = [r for r in results_normal if r["success"]]
    rate_normal = (len(succ_normal) / len(results_normal)) * 100
    gen_normal = sum(r["generations"] for r in succ_normal) / len(succ_normal) if succ_normal else "N/A"
    time_normal = sum(r["time"] for r in succ_normal) / len(succ_normal) if succ_normal else "N/A"
    print(f"  [Standard EA]  Success: {rate_normal}%, Gen: {gen_normal}, Time: {time_normal if isinstance(time_normal, str) else f'{time_normal:.4f}s'}")
    
    results_mutation = [functions.fit_mutation_only(n, child_count=20, mutation_prob=0.2, generations=5000) for _ in range(5)]
    succ_mut = [r for r in results_mutation if r["success"]]
    rate_mut = (len(succ_mut) / len(results_mutation)) * 100
    gen_mut = sum(r["generations"] for r in succ_mut) / len(succ_mut) if succ_mut else "N/A"
    time_mut = sum(r["time"] for r in succ_mut) / len(succ_mut) if succ_mut else "N/A"
    print(f"  [Mutation-only] Success: {rate_mut}%, Gen: {gen_mut}, Time: {time_mut if isinstance(time_mut, str) else f'{time_mut:.4f}s'}")
        
    results = [functions.fit_adaptive_mutation(n, child_count=20, generations=3000) for _ in range(5)]
    successful_runs = [r for r in results if r["success"]]
    success_rate = (len(successful_runs) / len(results)) * 100
    avg_gen = sum(r["generations"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
    avg_time = sum(r["time"] for r in successful_runs) / len(successful_runs) if successful_runs else "N/A"
    print(f"  [Adaptive-mutation] Success: {success_rate}%, Gen: {avg_gen}, Time: {avg_time if isinstance(avg_time, str) else f'{avg_time:.4f}s'}\n")
