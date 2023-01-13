from sqlite3 import Timestamp
from tokenize import String
from numpy import datetime_as_string
import pandas as pd
import pandas as np 
from datetime import datetime
from dateutil import relativedelta
from IPython.display import display


workers_time_id_resp = pd.read_csv(r'G:\uniud 2022 ULTIMO ANNO !!\social computing python\relazione 2\workers_answers.csv', 
                         usecols=['worker_id','time_submit_parsed','doc_id','doc_truthfulness-1_value','doc_truthfulness-2_value'])
# print(workers_time_id_resp)

workers_n = workers_time_id_resp.to_numpy()
workers_n_parsed = pd.DataFrame(workers_n, columns=["worker_id", "time", "doc_id", "doc_1_val","doc_2_val"])
# otteniamo le risposte per i primi worker e per i secondi workers 
workers_first_task = workers_n_parsed[["worker_id","doc_id","doc_1_val"]]
workers_second_task = workers_n_parsed[["worker_id","doc_id","doc_2_val"]]
# abbiamo notato che ci sono stati degli aggiornamenti della query, i valori 
# non ho trovato una veloce soluzione quindi lo droppo manualmente 
# problema nella riga 16 in conflitto con la riga 19 -> prevale la riga 19 per via del timestamp 
# problema nella riga 17 in conflitto con la riga 20 -> prevale la riga 20 (stessa motv)
# problema nella riga 18-21-22-23 -> prevale la riga 23 
# probelma nella riga 24 in conflitto con la riga 27-28 -> prevale la riga 24
# problema nella riga 25 in conflitto con 29 -> prevale la riga 25
# problema nella riga 26 in conflitto con 30 -> prevale la riga 26
workers_first_task = workers_first_task.drop([16,17,18,21,22,27,28,29,30])
workers_first_task = workers_first_task.reset_index(drop=True)

# valutiamo anche le seconde risposte 
# conflitto con riga 3 -> riga 7 --> vince la riga 7
# conflitto con riga 5 -> riga 9 --> vince la riga 5
# conflitto con riga 6 -> riga 8 --> vince la riga 8 
# conflitto con riga 16 -> riga 19 --> vince la riga 19 
# conflitto con riga 17 -> riga 20 --> vince la riga 20 
# conflitto con riga 18 - 21 - 22 - 23 -> vince la riga 23 
# conflitto con riga 24 - 27 - 28 -> vince la riga 24
# conflitto con riga 25 - 29 -> vince la riga 25
# conflitto con riga 26 - 30 -> vince la riga 26 
workers_second_task = workers_second_task.drop([3,9,6,16,17,18,21,22,27,28,29,30]).reset_index(drop=True)
workers_second_task = workers_second_task.set_index('worker_id')
#         risposta worker 
# doc_id  
# table document -> N_166632
# ricorda che per il numero di coppie totali possibili -> (n*(n-1))/2
def compute_percent_agreement(doc_id):
    doc_row = workers_second_task.loc[workers_second_task['doc_id'] == doc_id]
    doc_reset = doc_id.reset_index(level="worker_id")

    n_rows = doc_reset.shape[0]
    total_pairs = (n_rows*(n_rows-1))/2
    n_equal_pairs = 0
    
    for x in range(n_rows): 
        for y  in range(n_rows):
            if(x < y and doc_reset.at[x, "doc_2_val"] == doc_reset.at[y, "doc_2_val"]): 
                n_equal_pairs += 1
    return n_equal_pairs / total_pairs

doc_1 = workers_second_task.loc[workers_second_task['doc_id'] == 'N_166632']             # task -> N_166632
doc_2 = workers_second_task.loc[workers_second_task['doc_id'] == 'G_166632']             # task -> G_166632
doc_3 = workers_second_task.loc[workers_second_task['doc_id'] == 'N_51526']              # task -> N_51526
doc_4 = workers_second_task.loc[workers_second_task['doc_id'] == 'G_51526']              # task -> G_51526
doc_5 = workers_second_task.loc[workers_second_task['doc_id'] == 'N_77465']              # task -> N_77465
doc_6 = workers_second_task.loc[workers_second_task['doc_id'] == 'G_77465']              # task -> G_77465


# percentuale media di testo annotato -> quante volte appare la stessa istanza nella tabella - 1 
# workers_annotation = workers_time_id_resp.reset_index()
workers_annotation = workers_time_id_resp[["worker_id","doc_id"]]
workers_annotation = workers_annotation.groupby(['worker_id','doc_id']).size()


# Calcolate la percentuale media di testo annotato per ciascuna spiegazione
# Ordinate le spiegazioni sulla base di tale parametro 
quanto_hanno_annotato = pd.read_csv(r'G:\uniud 2022 ULTIMO ANNO !!\social computing python\relazione 2\workers_notes.csv', 
                                    usecols=['worker_id','document_index','note_text_current','note_text_left','note_text_right','note_timestamp_created'])
max_timestamp_ausiliario = quanto_hanno_annotato.groupby(by = ['worker_id','document_index'])['note_timestamp_created'].max().reset_index()





# ottenuti i dati di inizio e di fine -> fare la differenza

workers_time_diff = pd.read_csv(r'G:\uniud 2022 ULTIMO ANNO !!\social computing python\relazione 2\workers_answers.csv', 
                         usecols=['worker_id','doc_id','doc_time_elapsed'])

worker_one = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A348JKD82WQ6Z']     # worker uno A348JKD82WQ6Z
worker_two = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A3OAQZM6Q3YJQ1']    # worker due A3OAQZM6Q3YJQ1
worker_tree = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A1TEEFJDPVEK0L']    # worker tre A1TEEFJDPVEK0L
worker_four = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A3T2NTPGB3KNDS']   # worker 4 A3T2NTPGB3KNDS
worker_five = workers_time_diff.loc[workers_time_diff['worker_id'] == 'AYKZJHEV29ZHL']    # worker 5 AYKZJHEV29ZHL
worker_six = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A2Q51AC4E6I5ZB']    # worker 6 A2Q51AC4E6I5ZB
worker_seven = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A3W16X5D0VGU0E']  # worker 7 A3W16X5D0VGU0E
worker_eight = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A348JKD82WQ6Z']   # worker 8 A2Z4OTGC834F3Y
worker_nine = workers_time_diff.loc[workers_time_diff['worker_id'] == 'A2N1GA8PJDDA6P']   # worker 9 A2N1GA8PJDDA6P
worker_ten = workers_time_diff.loc[workers_time_diff['worker_id'] == 'AYUF9OHXQK2YT']     # worker 10 AYUF9OHXQK2YT

