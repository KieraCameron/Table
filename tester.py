import csv
from random import randint
from timeit import Timer

heading = ['atmosphere', 'bread', 'committee', 'disaster', 'entertainment', 'emphasis', 'temperature', 'history', 'instruction', 'revenue', 'country', 'dirt', 'comparison', 'science', 'stranger', 'community', 'member', 'procedure', 'historian', 'response', 'philosophy', 'fact', 'meaning', 'contribution', 'software', 'moment', 'beer', 'alcohol', 'drawing', 'variation', 'employment', 'user', 'newspaper', 'chemistry', 'buyer', 'championship', 'dealer', 'worker', 'environment', 'discussion', 'administration', 'village', 'apartment', 'product', 'soup', 'appearance', 'meal', 'television', 'construction', 'lab', 'president', 'arrival', 'physics', 'industry', 'idea', 'ladder', 'audience', 'wedding', 'potato', 'employer', 'assignment', 'agency', 'expression', 'quality', 'artisan', 'church', 'activity', 'pizza', 'knowledge', 'desk', 'fortune', 'nature', 'technology', 'region', 'surgery', 'literature', 'requirement', 'pie', 'topic', 'editor', 'insect', 'hat', 'exam', 'oven', 'son', 'poet', 'studio', 'wife', 'equipment', 'decision', 'person', 'opinion', 'income', 'sector', 'examination', 'education', 'hall', 'highway', 'success', 'grandmother', 'setting', 'map', 'gene', 'promotion', 'sir', 'device', 'mood', 'interaction', 'breath', 'shopping', 'context', 'skill', 'negotiation', 'grocery', 'actor', 'bathroom', 'republic', 'steak', 'situation', 'leadership', 'mud', 'information', 'reception', 'love', 'cousin', 'addition', 'chapter', 'category', 'drawer', 'aspect', 'solution', 'method', 'organization', 'family', 'food', 'drama', 'analysis', 'payment', 'bath', 'town', 'feedback', 'guest', 'percentage', 'apple', 'charity', 'instance', 'paper', 'debt', 'currency', 'estate', 'language', 'complaint', 'coffee', 'understanding', 'guidance', 'event', 'night', 'government', 'photo', 'road', 'media', 'goal', 'relationship', 'direction', 'city', 'way', 'basis', 'improvement', 'two', 'speaker', 'salad', 'perspective', 'phone', 'maintenance', 'transportation', 'hotel', 'tongue', 'blood', 'tradition', 'trainer', 'analyst', 'art', 'baseball', 'cheek', 'responsibility', 'fishing', 'mode', 'politics', 'tale', 'ad', 'policy', 'replacement', 'entry', 'operation', 'economics', 'storage', 'communication', 'management', 'theory', 'nation', 'importance', 'recording', 'freedom', 'orange', 'judgment', 'hair', 'definition', 'society', 'piano', 'song', 'proposal', 'assistance', 'unit', 'collection', 'location', 'magazine', 'marriage', 'player', 'election', 'platform', 'teaching', 'funeral', 'role', 'argument', 'outcome', 'law', 'writing', 'system', 'singer', 'confusion', 'reputation', 'departure', 'penalty', 'description', 'selection', 'failure', 'thanks', 'injury', 'difference', 'article', 'impression', 'contract', 'camera', 'health', 'disease', 'obligation', 'month', 'childhood', 'database', 'population', 'people', 'chest', 'medicine', 'honey', 'supermarket', 'attention', 'enthusiasm', 'bird', 'passion', 'area', 'opportunity', 'garbage', 'hospital', 'candidate', 'ability', 'measurement', 'friendship', 'manager', 'winner', 'concept', 'reading', 'possession', 'meat', 'series', 'computer', 'math', 'department', 'presence', 'delivery', 'throat', 'attitude', 'awareness', 'child', 'message', 'emotion', 'sympathy', 'weakness', 'recommendation', 'king', 'profession', 'accident', 'membership', 'professor', 'thing', 'union', 'advertising', 'courage', 'girl', 'difficulty', 'office', 'satisfaction', 'error', 'homework', 'bonus', 'cookie', 'engine', 'teacher', 'director', 'ear', 'memory', 'depth', 'restaurant', 'college', 'housing', 'intention', 'efficiency', 'army', 'secretary', 'session', 'writer', 'cigarette', 'inflation', 'signature', 'vehicle', 'poetry', 'criticism', 'variety', 'girlfriend', 'airport', 'music', 'assistant', 'student', 'application', 'mall', 'university', 'police', 'painting', 'climate', 'reflection', 'safety', 'truth', 'assumption', 'engineering', 'clothes', 'tooth', 'growth', 'basket', 'statement', 'sample', 'warning', 'insurance', 'development', 'bedroom', 'inspection', 'year', 'control', 'poem', 'distribution', 'patience', 'disk', 'cancer', 'initiative', 'appointment', 'manufacturer', 'passenger', 'youth', 'effort', 'advice', 'mom', 'speech', 'permission', 'lady', 'protection', 'data', 'preference', 'connection', 'resolution', 'wood', 'elevator', 'loss', 'pollution', 'refrigerator', 'suggestion', 'strategy', 'explanation', 'conclusion', 'video', 'version', 'priority', 'sister', 'imagination', 'leader', 'library', 'lake', 'introduction', 'world', 'combination', 'possibility', 'cabinet', 'recipe', 'client', 'cell', 'death', 'establishment', 'perception', 'boyfriend', 'property', 'river', 'reality', 'height', 'volume', 'ambition', 'indication', 'relation', 'revolution', 'mixture', 'diamond', 'independence', 'security', 'internet', 'woman', 'menu', 'story', 'virus', 'anxiety', 'agreement', 'flight', 'extent', 'celebration', 'foundation', 'birthday', 'recognition', 'affair', 'wealth', 'chocolate', 'tennis', 'owner', 'preparation', 'ratio', 'scene', 'driver', 'inspector', 'dinner', 'length', 'excitement', 'uncle', 'presentation', 'hearing', 'personality', 'performance', 'customer', 'investment', 'energy', 'county', 'resource', 'finding', 'tea', 'week', 'dad', 'problem', 'movie', 'reaction']
heading_set = set(heading)
alphabet = "".join(sorted("qwertyuiopasdfghjklzxcvbnm"))
def increment(word):
    if word == "":
        return alphabet[0]
    last = word[-1]
    index = alphabet.index(last)
    if index == 25:
        return increment(word[:-1]) + alphabet[0]
    else:
        return word[:-1] + alphabet[index+1]

def get_row(word):
    return [word] + [randint(1, 1000000) for x in range(len(heading))]

row_id = ""
data = list()
with open("test.csv", "w") as rawfile:
    csvfile = csv.writer(rawfile)
    csvfile.writerow(heading)
    lines = 0
    tt = Timer()
    for i in range(1000000):
        if (i+1) % 100000 == 0:
            print(i//100000, timeits[-1] - timeits[-2])
        row_id = increment(row_id)
        while row_id in heading_set:
            row_id = increment(row_id)
        data.append(get_row(row_id))
    csvfile.writerows(data)
    print(Timer() - tt)
