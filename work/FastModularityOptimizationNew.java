package admin;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashMap;

//import org.apache.logging.log4j.LogManager;
//
//import com.yangliu.util.FileEncodeUtil;

/// <summary>
/// 本算法是基于08年的快速算法：Fast unfolding of communities in large networks
/// </summary>
public class FastModularityOptimizationNew {
//	private static org.apache.logging.log4j.Logger logger = LogManager
//			.getLogger(Modularity.class.getName());
	// 控制顶点与边容量参数
	public static int node_params = 3000000;
	public static int edge_params = 5000000;

	// 存储网络的基本信息
	// 存储网络中的边
	public List<Integer> start = new ArrayList<Integer>(edge_params);
	public List<Integer> end = new ArrayList<Integer>(edge_params);
	// 存储网络中边的权值
	public List<Integer> weight = new ArrayList<Integer>(edge_params);
	public List<Double> weight_sim = new ArrayList<Double>(edge_params);
	// 存储网络中的顶点
	public HashSet<Integer> nodes = new HashSet<Integer>();
	// 顶点最大编号
	public int MAX_NODE_ID = 0;
	// 网络边数
	public int TOTAL_EDGE_NUMBER = 0;
	// 转移次数
	public int transfer_number = 0;

	// 邻接矩阵与权值矩阵
	// 邻接矩阵
	public List<List<Integer>> adjacent_matrix = new ArrayList<List<Integer>>(
			node_params);
	// 权值矩阵
	public List<List<Integer>> weight_matrix = new ArrayList<List<Integer>>(
			node_params);
	public List<List<Double>> weight_matrix_sim = new ArrayList<List<Double>>(
			node_params);

	// 算法变量
	// 顶点度数
	public List<Integer> node_degree = new ArrayList<Integer>(node_params);
	// 社团度数
	public List<Integer> community_degree = new ArrayList<Integer>(node_params);
	// 顶点所属社团号
	public List<Integer> node_to_community = new ArrayList<Integer>(node_params);
	// 社团
	public List<List<Integer>> communities = new ArrayList<List<Integer>>(
			node_params);
	// 顶点访问标记
	public List<Boolean> node_visited_state = new ArrayList<Boolean>(
			node_params);
	// 未使用的社团号
	public List<Integer> unused_community_id = new ArrayList<Integer>();

	// 从文件读取网络
	// 分析：初始化时，未使用社团号列表为空，列表中的社团号只可能来自顶点本身的ID
	public void read_from_file(String path) {
		List<String> lines = FileEncodeUtil.read(path);
		for (String line : lines) {
			String[] str = line.split(" ");
			int node1 = Integer.parseInt(str[0]);
			int node2 = Integer.parseInt(str[1]);
			int w = Integer.parseInt(str[2]);
			start.add(node1);
			end.add(node2);
			weight.add(w);
			weight_sim.add(0.0);
			nodes.add(node1);
			nodes.add(node2);
			if (node1 > MAX_NODE_ID)
				MAX_NODE_ID = node1;
			if (node2 > MAX_NODE_ID)
				MAX_NODE_ID = node2;
			TOTAL_EDGE_NUMBER++;
		}
		// 读入顶点的社团分配号
		for (int i = 0; i <= MAX_NODE_ID; i++)
			node_to_community.add(i);

		// 注：此处默认动态网络中的所有顶点

//		logger.info("nodes:" + nodes.size() + ",edges:" + TOTAL_EDGE_NUMBER);

	}

	// 初始化网络数据结构
	public void init() {
		for (int i = 0; i <= MAX_NODE_ID; i++) {
			// 初始化邻接矩阵与权值矩阵
			adjacent_matrix.add(new ArrayList<Integer>());
			weight_matrix.add(new ArrayList<Integer>());
			weight_matrix_sim.add(new ArrayList<Double>());
			// 初始化顶点度数与社团度数
			node_degree.add(0);
			community_degree.add(0);
			// 初始化顶点访问标记
			node_visited_state.add(false);
			// 初始化社团列表
			communities.add(new ArrayList<Integer>());
		}

		// 初始化顶点的社团
		// 将同一个社团的顶点加合并到一起
		for (int e : nodes) {
			int cc = node_to_community.get(e);
			communities.get(cc).add(e);
		}
	}

	// 邻接矩阵与权值矩阵
	public void adjacent_weight_construct() {
		for (int e : nodes) {
			adjacent_matrix.get(e).clear();
			weight_matrix.get(e).clear();
		}

		for (int i = 0; i < start.size(); i++) {
			int node1 = start.get(i);
			int node2 = end.get(i);
			int weight_value = weight.get(i);
			// double weight_value_sim = weight_sim.get(i);

			adjacent_matrix.get(node1).add(node2);
			weight_matrix.get(node1).add(weight_value);

			adjacent_matrix.get(node2).add(node1);
			weight_matrix.get(node2).add(weight_value);
		}

	}
	// 计算顶点的度与社团的度

	public void node_community_degree() {
		// 第一次迭代使用这个函数
		for (int i = 0; i <= MAX_NODE_ID; i++) {
			// int number = adjacent_matrix.get(i).size();
			List<Integer> neighbors = adjacent_matrix.get(i);
			int length = neighbors.size();
			for (int index = 0; index < length; index++)
				node_degree.set(i, node_degree.get(i)+ weight_matrix.get(i).get(index));
			int group_id = node_to_community.get(i);
			community_degree.set(group_id, community_degree.get(group_id)+ node_degree.get(i));
		}
	}

	// 超级节点产生后使用这个函数
	public void super_node_community_degree() {
		// 此处的顶点e属于社团中的一个，作为代表
		for (int e : nodes) {
			int community_e = node_to_community.get(e);
			node_degree.set(e, community_degree.get(community_e));
		}

	}
	// 挑选邻居顶点

	public boolean choose_max_modularity() {
		boolean flag = false;
		double max_value = 0;
		int max_community_id = 0;
		int edge_e_e = 0;
		int edge_e_nb = 0;
		double modularity_delta = 0.0;
		Map<Integer, Integer> node_links = new HashMap<Integer, Integer>();
		HashSet<Integer> comm_id = new HashSet<Integer>();
		List<Integer> order_list = new ArrayList<Integer>();
		order_list.addAll(nodes);
		Collections.sort(order_list, Collections.reverseOrder());
		for (int e : order_list) {
			double degree_e = 1.0 * node_degree.get(e);
			if (degree_e == 0) {
				int group_id = node_to_community.get(e);
				int group_id_degree = community_degree.get(group_id);
				if (group_id_degree != 0) {
					int assign_community_id = unused_community_id.get(0);
					unused_community_id.remove(0);
					node_to_community.set(e, assign_community_id);
				}
			} else {
				max_value = 0;
				List<Integer> neighbors = adjacent_matrix.get(e);
				int neighbors_length = neighbors.size();
				int community_id_e = node_to_community.get(e);
				max_community_id = community_id_e;
				node_links.clear();
				comm_id.clear();

				// 存储邻居的社团号
				for (int cc : neighbors) {
					comm_id.add(node_to_community.get(cc));
				}
				comm_id.add(community_id_e);

				// 临时添加邻居的社团号
				for (int cc_key : comm_id)
					node_links.put(cc_key, 0);

				// 计算顶点e与各个社团的连边权重
				for (int i = 0; i < neighbors_length; i++) {
					int nb_id = neighbors.get(i);
					int community_id_nb = node_to_community.get(nb_id);
					node_links.put(community_id_nb,node_links.get(community_id_nb)+ weight_matrix.get(e).get(i));

				}

				// 顶点e与社团的连边
				edge_e_e = node_links.get(community_id_e);

				double degree_community_e = 1.0 * community_degree
						.get(community_id_e);

				// 顶点e转移到一个空社团的模块度增量
				double new_modularity_value = ((degree_community_e - degree_e) * degree_e)
						/ (2.0 * TOTAL_EDGE_NUMBER * TOTAL_EDGE_NUMBER)
						- edge_e_e / (1.0 * TOTAL_EDGE_NUMBER);

				// int new_modularity_value = -1;
				// 从邻居里挑选一个最大的模块度增量
				for (int nb : neighbors) {

					int community_id_nb = node_to_community.get(nb);
					if (community_id_e != community_id_nb) {
						edge_e_nb = node_links.get(community_id_nb);
						double degree_commmunity_nb = 1.0 * community_degree
								.get(community_id_nb);

						modularity_delta = (edge_e_nb - edge_e_e)
								/ (1.0 * TOTAL_EDGE_NUMBER)
								- (degree_e * (degree_e + degree_commmunity_nb - degree_community_e))
								/ (2.0 * TOTAL_EDGE_NUMBER * TOTAL_EDGE_NUMBER);

						if ((modularity_delta > max_value)) {
							max_value = modularity_delta;
							max_community_id = community_id_nb;
						}
					}
				}

				if (max_value > 0 && max_value > new_modularity_value) {
					flag = true;
					// 改变node1与node2所在社团的度数
					community_degree.set(community_id_e,community_degree.get(community_id_e)- node_degree.get(e));
					community_degree.set(max_community_id,community_degree.get(max_community_id)+ node_degree.get(e));
					// 改变顶点e的社团编号
					node_to_community.set(e, max_community_id);
					if (community_degree.get(community_id_e) == 0)
						unused_community_id.add(community_id_e);
					transfer_number++;
				}

				else if (new_modularity_value > 0) {
					// 能进入这里面，e的社团至少包含两个顶点
					flag = true;
					// 分配社团号
					int assign_community_id = unused_community_id.get(0);
					unused_community_id.remove(0);
					node_to_community.set(e, assign_community_id);
					community_degree.set(community_id_e,community_degree.get(community_id_e)- node_degree.get(e));
					community_degree.set(assign_community_id,community_degree.get(assign_community_id)+ node_degree.get(e));
					transfer_number++;
				}
			}
		}
		return flag;
	}

	// 新网络的顶点ID
	public void new_network_node_id(Map<Integer, Integer> new_node_id) {
		HashSet<Integer> new_nodes = new HashSet<Integer>();
		// 取出顶点所在的超级顶点号
		for (int e : nodes) {
			new_nodes.add(node_to_community.get(e));
		}
		for (int e : new_nodes)
			new_node_id.put(e, 0);
		for (int e : nodes) {
			int community_node_id = node_to_community.get(e);
			new_node_id.put(community_node_id, e);

		}
	}

	// 构造新网络的边数
	public void construct_new_network(List<String> all_new_edges,
			Map<Integer, Integer> new_node_id) {
		for (int e : nodes) {
			List<Integer> neighbors = adjacent_matrix.get(e);
			int neighbors_length = neighbors.size();
			int community_e_name = node_to_community.get(e);
			int node1_community_id = new_node_id.get(community_e_name);
			for (int i = 0; i < neighbors_length; i++) {
				int nb = neighbors.get(i);
				int community_nb_name = node_to_community.get(nb);
				int node2_community_id = new_node_id.get(community_nb_name);
				if (e < nb && node1_community_id != node2_community_id) {
					int nb_weight = weight_matrix.get(e).get(i);
					for (int j = 0; j < nb_weight; j++) {
						if (node1_community_id < node2_community_id){
							all_new_edges.add(node1_community_id + " "+ node2_community_id);
//							logger.info("1:"+node1_community_id + " "+ node2_community_id);
						}
						else{
							all_new_edges.add(node2_community_id + " "+ node1_community_id);
//							logger.info("2:"+node2_community_id + " "+ node1_community_id);
						}
					}
				}
			}
		}
	}

	// 社团划分
	public void community_partition(Map<Integer, Integer> new_node_id) {
		// 搜索顶点的社团号
		for (int e : nodes) {
			int community_e_id = node_to_community.get(e);
			int container_id = new_node_id.get(community_e_id);
			List<Integer> member = communities.get(e);
			if (container_id != e) {
				for (int mb : member)
					communities.get(container_id).add(mb);
				communities.get(e).clear();
			}
		}
	}

	// 读取新网络
	public void read_new_network(List<String> all_new_edges,
			Map<Integer, Integer> new_node_id) {
		start.clear();
		end.clear();
		weight.clear();

		HashSet<Integer> new_nodes = new HashSet<Integer>();
		for (int e : nodes)
			new_nodes.add(node_to_community.get(e));
		nodes.clear();
		for (int e : new_nodes) {
			int new_node = new_node_id.get(e);
			nodes.add(new_node);
		}
		Set<String> groups = new HashSet<String>();
		groups.addAll(all_new_edges);

//		 for(String a:all_new_edges)
//		 logger.info("a:"+a);
		 
		// int groups = all_new_edges.GroupBy(a => a);
		/*
		 * Console.WriteLine("yangliu:"); foreach (int x in all_new_edges) {
		 * Console.WriteLine(x); } Console.WriteLine("original:");
		 */
		for (String e : groups) {
			String[] two_nodes = e.split(" ");
			int node1 = Integer.parseInt(two_nodes[0]);
			int node2 = Integer.parseInt(two_nodes[1]);
			//logger.info("e:" + e);
			int edge_weight = e.length();
			start.add(node1);
			end.add(node2);
			weight.add(edge_weight);
			nodes.add(node1);
			nodes.add(node2);
		}
	}

	// 计算网络模块度

	public double compute_network_modularity() {
		double average_edges = 0;
		int inner_edges = 0;
		double modularity = 0.0;
		for (int e : nodes) {
			average_edges += (1.0 * node_degree.get(e) * node_degree.get(e));
			List<Integer> neighbors = adjacent_matrix.get(e);
			int neighbors_length = neighbors.size();
			for (int i = 0; i < neighbors_length; i++) {
				int nb = neighbors.get(i);
				if (e < nb)
					inner_edges += weight_matrix.get(e).get(i);

			}
		}

		inner_edges = TOTAL_EDGE_NUMBER - inner_edges;
		int total_degree = 2 * TOTAL_EDGE_NUMBER;
		modularity = (inner_edges / (1.0 * TOTAL_EDGE_NUMBER)) - average_edges
				/ (4.0 * TOTAL_EDGE_NUMBER * TOTAL_EDGE_NUMBER);
//		logger.info("communities number:" + nodes.size() + "  modularity:"
//				+ modularity);
		return modularity;
	}

	public void compute_step_modularity() {
		double average_edges = 0;
		int inner_edges = 0;
		double modularity = 0.0;
		HashSet<Integer> community_id_list = new HashSet<Integer>();
		community_id_list.clear();
		for (int e : nodes)
			community_id_list.add(node_to_community.get(e));

		for (int e : community_id_list)
			average_edges += (1.0 * community_degree.get(e) * community_degree
					.get(e)) / (4.0 * TOTAL_EDGE_NUMBER * TOTAL_EDGE_NUMBER);
		for (int e : nodes) {
			List<Integer> neighbors = adjacent_matrix.get(e);
			int neighbors_length = neighbors.size();
			int community_e_id = node_to_community.get(e);
			for (int i = 0; i < neighbors_length; i++) {
				int nb = neighbors.get(i);
				int community_nb_id = node_to_community.get(nb);
				if (e < nb && (community_e_id != community_nb_id))
					inner_edges += weight_matrix.get(e).get(i);

			}
		}

		inner_edges = TOTAL_EDGE_NUMBER - inner_edges;
		int total_degree = 2 * TOTAL_EDGE_NUMBER;
		modularity = (inner_edges / (1.0 * TOTAL_EDGE_NUMBER)) - average_edges;
//		logger.info("modularity:" + modularity + " inner edges:" + inner_edges
//				+ " out edges:" + (TOTAL_EDGE_NUMBER - inner_edges));

	}

	// 输出社团
	public void output_community(String filename) {
		File file = FileEncodeUtil.cleanFile(filename);
		for (int e : nodes) {
			// System.out.println("list:"+e);
			List<Integer> orger_groups = communities.get(e);
			Collections.sort(orger_groups);
			// 当簇内的元素个数大于3时输出
			// if(orger_groups.size()>=3){
			for (int c : orger_groups)
				FileEncodeUtil.write(file, c + " ");
			FileEncodeUtil.write(file, "\n");
			// }

		}
//		logger.info("communities number:" + nodes.size());
	}

	// 程序执行

	public void execute(String path, String filename) {

		read_from_file(path);
		init();
		boolean first_iterate = true;
		boolean quit_flag = false;
		Map<Integer, Integer> new_node_id = new HashMap<Integer, Integer>();
		List<String> all_new_edges = null;
		while (true) {
			quit_flag = true;
			;
			adjacent_weight_construct();
			if (first_iterate) {
				node_community_degree();
				first_iterate = false;
			} else
				super_node_community_degree();

			// 调整顶点之间的组合，直到所有顶点无法移动为止
			while (true) {
				// 遍历一次所有顶点，并返回是否有顶点移动的标志
				boolean merge_flag = choose_max_modularity();
				// 表示这次无任何顶点移动，可以重构网络
				if (merge_flag) {
					// 如果有顶点移动过，则不用退出
					quit_flag = false;
					compute_step_modularity();
				} else
					break;
			}

			// 如果为真，则表示第一次遍历就无任何顶点移动，则程序可以结束
			// 如果为假，则表示存在顶点移动的情况发生
			if (quit_flag)
				break;
			else {
				new_node_id.clear();
				new_network_node_id(new_node_id);
				community_partition(new_node_id);
				all_new_edges = new ArrayList<String>();
				construct_new_network(all_new_edges, new_node_id);
				read_new_network(all_new_edges, new_node_id);
				// fmo.output_community();
			}
		}

		// 输出社团
		output_community(filename);

	}

//	public static void main(String[] args) {
////		String file_path = "graph-prun/graph-prun_0.txt";
//		ArrayList<String> list = new ArrayList<>();
//		list.add("06");
//		list.add("07");
//		list.add("08");
//		list.add("09");
//		list.add("10");
//		list.add("11");
//		list.add("12");
//		list.add("13");
//		list.add("14");
//		list.add("15");
//		list.add("16");
//		list.add("17");
//		for (String year:list) {
//			String file_path = "F:\\classify_data\\newMaterials\\title_fos\\title_fos" + year + "_both_words_result1.txt";
//			String result_path = "F:\\classify_data\\newMaterials\\title_fos\\title_fos" + year + "_both_words_new_result.txt";
//			new FastModularityOptimizationNew().execute(file_path, result_path);
//			System.out.print(" finish file : " + year+"\n");
//		}
//	}

//	public static void main(String[] args) {
////		String file_path = "graph-prun/graph-prun_0.txt";
//		String file_path = "F:\\classify_data\\newMaterials\\title_fos\\fos_title_every_year_data_both_exist.txt";
//		String result_path = "F:\\classify_data\\newMaterials\\title_fos\\fos_title_every_year_data_both_exist_new_result.txt";
//		new FastModularityOptimizationNew().execute(file_path, result_path);
//	}

	public static void main(String[] args) {
//		String file_path = "graph-prun/graph-prun_0.txt";
		String file_path = "F:\\classify_data\\newMaterials\\cluster_data_net\\index_name_net_36.txt";
		String result_path = "F:\\classify_data\\newMaterials\\cluster_data_net\\index_name_net_36_new_result.txt";
		new FastModularityOptimizationNew().execute(file_path, result_path);
	}

}
