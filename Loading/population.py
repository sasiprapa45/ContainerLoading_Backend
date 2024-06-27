from .placement import Placement
from .datac import get__project, get_container_by_project_id,get_cargoes_by_project_id
import random
import heapq
import itertools

class Chromosome:
    def __init__(self, gene, fitness, gene_data, boxes, con_use,weight_pk):
        self.gene = gene
        self.fitness = fitness
        self.gene_data = gene_data
        self.boxes = boxes
        self.con_use = con_use
        self.weight_pk = weight_pk

    def get_Gene(self):
        return self.gene
    def get_Gene_Data(self):
        return self.gene_data
    def set_InToFitness(self, fit):
        self.fitness = fit
    def get_Fitness(self):
        return self.fitness
    def get_boxes(self):
        return self.boxes
    
def random_Chromosome(box):
    new = box.copy()
    random.shuffle(new)  # สลับค่าในอาร์เรย์
    return new

def generate_all_permutations(original_array):
    return list(itertools.permutations(original_array))

def pmx(parent1, parent2):
    size = len(parent1)
    p1, p2 = parent1[:], parent2[:]
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))

    def pmx_crossover(p1, p2):
        child = [None] * size
        # Copy the slice from the first parent
        child[cxpoint1:cxpoint2] = p1[cxpoint1:cxpoint2]

        # Fill the rest with the values from the second parent
        for i in range(cxpoint1, cxpoint2):
            if p2[i] not in child:
                for j in range(size):
                    if child[j] is None:
                        if p2[j] not in child:
                            child[j] = p2[i]
                            break

        # Fill in the remaining None values
        for i in range(size):
            if child[i] is None:
                child[i] = p2[i]

        # Fix duplicates by replacing them with missing elements
        child_ids = {item['id'] for item in child}
        missing_elements = [item for item in parent1 if item['id'] not in child_ids]

        for i in range(size):
            if child.count(child[i]) > 1:
                child[i] = missing_elements.pop(0)
        
        return child

    child1 = pmx_crossover(p1, p2)
    child2 = pmx_crossover(p2, p1)

    return child1, child2

def crossover(parent1, parent2):
    child1, child2 = pmx(parent1, parent2)

    mutation_rate = 0.001
    child1 = mutation(child1, mutation_rate)
    child2 = mutation(child2, mutation_rate)
    return child1, child2

def mutation(chromosome, mutation_rate):
    # Choose a random crossover point
    mutated_chromosome = chromosome[:]  # สร้างสำเนาของโครโมโซมเพื่อป้องกันการเปลี่ยนแปลงต้นฉบับ

    if random.random() < mutation_rate:
        # ทำการกลายพันธุ์ที่ตำแหน่งนี้
        # สลับตำแหน่งของสมาชิกสองตำแหน่งในลำดับ
        idx1,idx2= random.sample(range(len(chromosome)), 2)
        gene_random = mutated_chromosome[idx1]
        mutated_chromosome[idx1]=  mutated_chromosome[idx2]
        mutated_chromosome[idx2] = gene_random

    return mutated_chromosome

# print(gene)
# for g in gene:  # วนรอบเพื่อเข้าถึงแต่ละอ็อบเจ็กต์ Cargos
#     print(g)

def Population(Pid):
    con = get_container_by_project_id(Pid)
    container_data = len(con)
    gene = get_cargoes_by_project_id(Pid)
    cargoes_data = len(gene)
    project = get__project(Pid)
    p_ck_weight = project['weight_check']
    population = []
    fit = 0
    best_fitness = -float('inf')
    best_fitness_con = -float('inf')
    # best_chromosome = None
    no_improvement_count = 0
    no_improvement_count_con = 0
    max_no_improvement = 50
    max_no_improvement_con = 10
    
    # for c in con:
    #     print(c['weight_pack'])
    # print(len(con))
    print(gene)
    # print(len(gene))
    # print("---------------------------------------------------------------------------------------------------------")
    for i in range(1,200):
        g = random_Chromosome(gene)
        ids = map(lambda x: x['id'], g)
        print(list(ids))
        print("---------------------------------------------------------------------")
        boxes_data,fit,boxes,con_use,weight = Placement(g,con,p_ck_weight)
        population.append(Chromosome(g,fit, boxes_data,boxes,con_use,weight))



#-------------cross--------------------------
    all_permutations = generate_all_permutations(con)
    for con_permutation in all_permutations:
        # แปลง tuple ให้เป็น list
        con = list(con_permutation)
        while True:
            best_fitness_con = best_fitness
            population.sort(key=lambda chromosome: chromosome.fitness)
            parent1 = population[-1].gene
            parent2 = population[-2].gene
            child1, child2 = crossover(parent1, parent2)
            ids1 = map(lambda x: x['id'], child1)
            ids2 = map(lambda x: x['id'], child2)
            print(list(ids1))
            print("-----------next child2---------")
            print(list(ids2))
            print("---------------------------------------------------------------------")
            boxes_data1,fit1,boxes1,con_use1,weight1 = Placement(child1,con,p_ck_weight)
            boxes_data2,fit2,boxes2,con_use2,weight2 = Placement(child2,con,p_ck_weight)
            population.append(Chromosome(child1, fit1, boxes_data1,boxes1,con_use1,weight1))
            population.append(Chromosome(child2, fit2, boxes_data2,boxes2,con_use2,weight2))
            if fit1 > best_fitness :
                best_fitness = fit1
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if fit2 > best_fitness:
                best_fitness = fit2
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            if no_improvement_count >= max_no_improvement:
                break
        if best_fitness > best_fitness_con :
            no_improvement_count_con = 0
        else:
            best_fitness = best_fitness_con
            no_improvement_count_con += 1

        if no_improvement_count_con >= max_no_improvement_con:
            break
        # print("Parent 1:", parent1)
        # print("Parent 2:", parent2)
        # print("Child 1:", child1)
        # print("Child 2:", child2)
        # print("*****************************************************************************************************")

    # for p in population:  # วนรอบเพื่อเข้าถึงแต่ละอ็อบเจ็กต์ Cargos
    #         print(p.gene)
    #         print(p.fitness)
    population.sort(key=lambda chromosome: chromosome.fitness)
    # print(population[-1].fitness)
    # print(population[1].fitness)
    # print("---------------------------------------------------------------------------------------------------------")
    # print(min(population, key=lambda chromosome: chromosome.fitness).fitness)
    # print(max(population, key=lambda chromosome: chromosome.fitness).fitness)
    # print(max(population, key=lambda chromosome: chromosome.fitness).fitness)
    # print("---------------------------------------------------------------------------------------------------------")
    # print(len(min(population, key=lambda chromosome: chromosome.fitness).gene_data))
    # print(len(max(population, key=lambda chromosome: chromosome.fitness).gene_data))
    # print(min(population, key=lambda chromosome: chromosome.fitness).gene_data)
    # print(population[0].gene_data)
    # print(len(max(population, key=lambda chromosome: chromosome.fitness).gene_data))
    # print("---------------------------------------------------------------------------------------------------------")
    # PlacementCargo(population[-1].gene,con)  #แสดงการจัดเรียง fitnessมากสุด
    # Plot_boxes(min(population, key=lambda chromosome: chromosome.fitness).boxes,con)
    # Plot_boxes(max(population, key=lambda chromosome: chromosome.fitness).boxes,con)  #แสดงการจัดเรียง fitnessมากสุด
    best_chromosome = max(population, key=lambda chromosome: chromosome.fitness)
    cargoes_packing = len(best_chromosome.gene_data)
    container_use = best_chromosome.con_use
    fitness = best_chromosome.fitness
    best_placement = best_chromosome.gene_data
    weight_pack = best_chromosome.weight_pk
    # print(best_placement)
    return best_placement,cargoes_data,cargoes_packing,container_data,container_use,fitness,weight_pack  #ส่งค่าให้ view หรือ api ที่เรียกมา 



