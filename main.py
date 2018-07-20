import abce
import pandas as pd
from firm import Firm
from people import People
import plotly.graph_objs as go
import plotly.offline as offline

def GraphFn(graphing_variable):
    """
    function that takes in graphing variable as parameter and the produces a graph
    using plotly
    """
    x_data = [[] for _ in range(params["num_firms"])]
    y_data = [[] for _ in range(params["num_firms"])]

    for i in range(len(df)):
        name = df["name"][i]
        number = int(name[4:])
        x_data[number].append(df["round"][i])
        y_data[number].append(df[graphing_variable][i])

    data = []    

    for i in range(params["num_firms"]):
        data.append(go.Scatter(x = x_data[i],
                            y = y_data[i],
                            mode = "lines"))
                            #name = ("firm" + str(i))))
            
    offline.init_notebook_mode(connected=True)
    offline.iplot(data)

def main(params): 
    simulation = abce.Simulation(name='economy', processes=1)
    group_of_firms = simulation.build_agents(Firm, "firm", number=params["num_firms"], **params)
    people = simulation.build_agents(People, "people", number=1, **params)
    
    for r in range(params["num_days"]):
        simulation.time = r

        group_of_firms.panel_log(variables=['wage', 'ideal_num_workers'], goods=['workers'])
        people.create_labor()

        vacancies_list = list(group_of_firms.publish_vacencies())

        people.send_workers(vacancies_list)

        group_of_firms.production()
        group_of_firms.pay_workers()
        group_of_firms.pay_dividents()
        group_of_firms.send_prices()
        people.get_prices()
        demand = people.buy_goods()

        group_of_firms.sell_goods()
        group_of_firms.determine_bounds(demand=list(demand)[0])
        (group_of_firms + people).print_possessions()
        group_of_firms.determine_wage()
        group_of_firms.expand_or_change_price()
        (people + group_of_firms).destroy_unused_labor()
        people.consumption()
        group_of_firms.determine_profits()

    print('done')
    path = simulation.path

    simulation.finalize()
 
    return sim_data = pd.read_csv(path + "/panel_firm.csv")