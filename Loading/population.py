from .placement import Placement
from .datac import get_container_by_project_id,get_cargoes_by_project_id
import random
import heapq

class Chromosome:
    def __init__(self, gene, fitness, gene_data, boxes):
        self.gene = gene
        self.fitness = fitness
        self.gene_data = gene_data
        self.boxes = boxes

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

def crossover(parent1, parent2):
    
    parent1_ids = [box['id'] for box in parent1]
    parent2_ids = [box['id'] for box in parent2]
    # Choose a random crossover point
    
    all_ids = list(set(parent1_ids + parent2_ids))
    
    # Randomly select crossover point
    crossover_point = random.randint(1, len(all_ids) - 1)
    
    # Select cargo IDs for crossover
    crossover_ids = all_ids[:crossover_point]
    child1 = [box for box in parent1 if box['id'] in crossover_ids] + [box for box in parent2 if box['id'] not in crossover_ids]
    child2 = [box for box in parent2 if box['id'] in crossover_ids] + [box for box in parent1 if box['id'] not in crossover_ids]
    # crossover_point = random.randint(1, len(parent1) - 1)

    # child1 = parent1[:crossover_point] + parent2[crossover_point:]

    # child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
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
    gene = get_cargoes_by_project_id(Pid)
    population = []
    fit = 0
    # print(len(con))
    # print(len(gene))
    # print("---------------------------------------------------------------------------------------------------------")
    for i in range(1,200):
        g = random_Chromosome(gene)
        boxes_data,fit,boxes = Placement(g,con)
        population.append(Chromosome(g,fit, boxes_data,boxes))


#-------------cross--------------------------
    for i in range(1,200):
        population.sort(key=lambda chromosome: chromosome.fitness)
        parent1 = population[-1].gene
        parent2 = population[-2].gene
        child1, child2 = crossover(parent1, parent2)
        boxes_data1,fit1,boxes1 = Placement(child1,con)
        boxes_data2,fit2,boxes2 = Placement(child2,con)
        population.append(Chromosome(child1, fit1, boxes_data1,boxes1))
        population.append(Chromosome(child2, fit2, boxes_data2,boxes2))
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
    print(min(population, key=lambda chromosome: chromosome.fitness).fitness)
    print(max(population, key=lambda chromosome: chromosome.fitness).fitness)
    # print(max(population, key=lambda chromosome: chromosome.fitness).fitness)
    # print("---------------------------------------------------------------------------------------------------------")
    print(len(min(population, key=lambda chromosome: chromosome.fitness).gene_data))
    print(len(max(population, key=lambda chromosome: chromosome.fitness).gene_data))
    # print(min(population, key=lambda chromosome: chromosome.fitness).gene_data)
    # print(population[0].gene_data)
    # print(len(max(population, key=lambda chromosome: chromosome.fitness).gene_data))
    # print("---------------------------------------------------------------------------------------------------------")
    # PlacementCargo(population[-1].gene,con)  #แสดงการจัดเรียง fitnessมากสุด
    # Plot_boxes(min(population, key=lambda chromosome: chromosome.fitness).boxes,con)
    # Plot_boxes(max(population, key=lambda chromosome: chromosome.fitness).boxes,con)  #แสดงการจัดเรียง fitnessมากสุด
    best_chromosome = max(population, key=lambda chromosome: chromosome.fitness)
    best_placement = best_chromosome.gene_data
    print(best_placement)
    return best_placement




