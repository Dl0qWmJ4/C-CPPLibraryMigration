import pandas as pd
import networkx as nx
import datetime
import math
import argparse

def parse_timestamp_with_offset(input_str):
    timestamp_str = input_str[:-5]
    timezone_offset_str = input_str[-5:]
    timestamp = int(timestamp_str)
    hours_offset = int(timezone_offset_str[:3])
    minutes_offset = int(timezone_offset_str[3:])
    total_offset = hours_offset + minutes_offset / 60
    utc_time = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    local_time = utc_time + datetime.timedelta(hours=total_offset)
    readable_date = local_time.strftime("%Y-%m-%d")
    return readable_date
 
def get_mig_info(commit_sha,migration_df):
    row = migration_df[migration_df['commit'] == commit_sha]
    if row.empty:
        return None
    
    row = row.iloc[0]
    mig_info = {
        'commit': row['commit'],
        'rem_lib': row['rem_lib'],
        'add_lib': row['add_lib'],
        'message': row['message'],
        'time_stamp': row['time_stamp'],
        'src': row['src'],
        'pattern': row['pattern'],
        'commit_url': row['commit_url'],
        'domain': row['domain'],
        'reason': row['reason']
    }
    return mig_info

def build_mig_graph(migration_df):
    G = nx.DiGraph()
    for _, row in migration_df.iterrows():
        commit = row['commit']
        add_lib = row['add_lib']
        rem_lib = row['rem_lib']
        if G.has_edge(rem_lib, add_lib):
            G[rem_lib][add_lib]['commits'].append(commit)
        else:
            G.add_edge(rem_lib, add_lib, commits=[commit])
    return G

def get_direct_lib(G, rem_lib):
    if rem_lib not in G:
        print(f"Library {rem_lib} not found in the graph.")
        return []

    direct_successors = list(G.successors(rem_lib))
    targeted = []
    for node in direct_successors:
        edge = (rem_lib, node)
        commits = G.edges[edge]['commits']
        targeted.append((node, [rem_lib, node], commits))
    
    return targeted

def get_iterative_lib(G, rem_lib):
    if rem_lib not in G:
        print(f"Library {rem_lib} not found in the graph.")
        return []
    
    reachables = list(nx.dfs_postorder_nodes(G, source=rem_lib))
    reachables.remove(rem_lib)
    
    direct_successors = set(G.successors(rem_lib))
    reachables = [node for node in reachables if node not in direct_successors]
    
    targeted = {}
    for node in reachables:
        paths = list(nx.all_simple_paths(G, source=rem_lib, target=node))
        for path in paths:
            commits = [G.edges[edge]['commits'] for edge in zip(path[:-1], path[1:])]
            if node not in targeted:
                targeted[node] = []
            targeted[node].append((path, commits))
    
    targeted_list = [(node, libs) for node, libs in targeted.items()]
    
    return targeted_list
    '''for reach in reachables:
        if rem_lib in reach:
            reachables.remove(reach)'''
    
def calculate_rank_score(mig_rec,migration_df):
    now = datetime.datetime.now()
    commits = mig_rec[2]
    rank_score = 0
    for commit in commits:
        time_stamp_str = get_mig_info(commit, migration_df)['time_stamp'][:-5] 
        time_stamp_num = pd.to_numeric(time_stamp_str)
        commit_time = pd.to_datetime(time_stamp_num, unit='s')
        
        month_diff = (now.year - commit_time.year) * 12 + now.month - commit_time.month
        if month_diff > 0:
            rank_score += 1/math.log(month_diff + 1)
    return rank_score

def direct_rec_rank(dir_targeted, migration_df, reason=None, pmt=None):
    priority_map = {1: [], 2: [], 3: [],4: []}

    for rec in dir_targeted:
        commit_infos = [get_mig_info(commit, migration_df) for commit in rec[2]]
        reason_match = src_match = 0
        for commmit in commit_infos:
            if str(reason) in str(commmit['reason']):
                reason_match = 1  
                break
        for commmit in commit_infos:
            if str(pmt) in str(commmit['src']):
                src_match = 1          
                break
        if reason_match:
            priority_map[1].append(rec)
        elif src_match:
            priority_map[2].append(rec)
        elif ',' in rec[0]:
            priority_map[3].append(rec)
        else:
            priority_map[4].append(rec)

    for priority in priority_map.values():
        priority.sort(key=lambda rec: calculate_rank_score(rec, migration_df), reverse=True)
        
    ranked_recs = priority_map[1] + priority_map[2] + priority_map[3] + priority_map[4]
    if not ranked_recs:
        ranked_recs = sorted(dir_targeted, key=lambda rec: calculate_rank_score(rec, migration_df), reverse=True)

    return ranked_recs

def put_targeted_lib(dir_rec,ite_rec, migration_df, reason=None, pmt=None, file_name='Targeted_Libraries.txt'):
    ranked_rec = direct_rec_rank(dir_rec, migration_df, reason, pmt)
    with open(file_name, 'w') as f:
        f.write(f"Targeted Libraries: ")
        rec_string = ", ".join([rec[0] if "," not in rec[0] else '[' + rec[0] + ']' for rec in ranked_rec ])
        f.write(rec_string)
        f.write(f"\n\n")
        for rec in ranked_rec:
            f.write(f"Targeted Library: {rec[0]}\n")
            f.write(f"Migration Rule: {' -> '.join(rec[1])}\n")
            f.write(f"Migration Frequency: {len(rec[2])}\n")
            f.write("Commits:\n")
            count = 0
            for commit in rec[2]:
                if count ==5:
                    break
                mig_info = get_mig_info(commit, migration_df)
                if mig_info:
                    f.write(f"  Commit SHA: {mig_info['commit']}\n")
                    f.write(f"  Commit URL: {mig_info['commit_url']}\n")
                    f.write(f"  Commit Message: {mig_info['message']}\n")
                    f.write(f"  Time: {parse_timestamp_with_offset(mig_info['time_stamp'])}\n")
                    f.write(f"  Reason: {mig_info['reason']}\n")
                    f.write(f"  Package Management Tool: {mig_info['src']}\n")
                    f.write("------\n")
                count += 1
            f.write("\n\n")
        f.write("------------------------------------------------------------------------------------------------------------------------\n\n\n")
        f.write(f"Iterative Targeted Library: ")
        rec_string = ", ".join([rec[0] for rec in ite_rec])
        f.write(rec_string)
        f.write(f"\n\n")
        for rec in ite_rec:
            f.write(f"Iterative Targeted Library: {rec[0]}\n")
            for i in rec[1]:
                f.write(f"Iterative Migration Rule: {' -> '.join(i[0])}\n")
            f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migration Library Query Tool")
    parser.add_argument('--rem_lib', required=True, help='Name of the library to remove')
    parser.add_argument('--reason', required=False, help='Reason for the library migration')
    parser.add_argument('--pmt', required=False, help='Package Manage Tool for the library migration')

    args = parser.parse_args()

    rem_lib = args.rem_lib
    reason = args.reason
    pmt = args.pmt

    mig_df = pd.read_csv('knowledge_base.csv')
    G = build_mig_graph(mig_df)

    iterative_targeted = get_iterative_lib(G, rem_lib)
    direct_targeted = get_direct_lib(G, rem_lib)

    put_targeted_lib(direct_targeted, iterative_targeted , mig_df, reason = reason, pmt = pmt)