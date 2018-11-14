import matplotlib.pyplot as plt


def file_read(num):
    get_list = []
    get_directory = 'execute_'+str(num)+'process/process_result.csv'
    print(get_directory)
    with open(get_directory,'r') as f:
        data = f.readline()
        while len(data)>0:
            data = data.replace('\n','')
            print(data)
            get_list.append(float(data))
            data = f.readline()
    return get_list

def visualize():
    client_10_list=file_read(10)
    client_20_list=file_read(20)
    client_30_list=file_read(30)

    box_plot_data = [client_10_list,client_20_list,client_30_list]
    plt.boxplot(box_plot_data)
    plt.xlabel("Numboer Of Clients")
    plt.ylabel("Donwload Time(s)")
    plt.xticks([1,2,3],[10,20,30])
    plt.show()
    

visualize()
