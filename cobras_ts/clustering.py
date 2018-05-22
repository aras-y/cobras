import collections


class Clustering:

    def __init__(self,clusters):
        self.clusters = clusters

    def construct_cluster_labeling(self):

        pts_per_cluster = [cluster.get_all_points() for cluster in self.clusters]

        pred = [-1] * sum([len(x) for x in pts_per_cluster])

        for i, pts in enumerate(pts_per_cluster):
            for pt in pts:
                pred[pt] = i

        return pred

    def traverse_tree_add_if_same_cluster(self, si):
        leaves = si.get_leaves()

        all_in_same_cluster = True
        cur_cluster = None
        for c in self.clusters:
            if leaves[0] in c.super_instances:
                cur_cluster = c
                break

        for l in leaves:
            if l not in cur_cluster.super_instances:
                all_in_same_cluster = False
                break

        if all_in_same_cluster:
            return leaves
        else:
            generalized_leaves = []
            for l in si.children:
                generalized_leaves.append(self.traverse_tree_add_if_same_cluster(l))
            return generalized_leaves

    def get_generalized_super_instances(self):
        # first get the generalized leaves
        generalized_super_instance_sets = self.traverse_tree_add_if_same_cluster(self.clusters[0].super_instances[0].get_root())

        # now map each cluster to its leaves
        cluster_to_si = collections.defaultdict(list)
        for cluster in self.clusters:
            to_delete = []
            for l in generalized_super_instance_sets:
                if l[0] in cluster.super_instances:
                    cluster_to_si[cluster].append(l)
                    to_delete.append(l)

            for l in to_delete:
                generalized_super_instance_sets.remove(l)

        return generalized_super_instance_sets




