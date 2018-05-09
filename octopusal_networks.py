
# coding: utf-8

class Octopus:

    shocks_threshold = 2

    def __init__(self, id):
        self.id = id
        self.awake = False
        self.excitement = 0
        self.tentacles = []

    def shocked(self, power):
        self.excitement += power
        if (self.excitement >= Octopus.shocks_threshold):
            self.awake = True

    def detail(self):
        result = f'{self}\n'
        for tentacle in self.tentacles:
            result += f'\t{tentacle}\n'
        return result

    def __str__(self):
        return f'Octopus {self.id} [awake: {self.awake}, excitement: {self.excitement}]'


# In[6]:


class Tentacle:

    def __init__(self, id, owner, connected):
        self.id = id
        self.owner = owner
        self.connected = connected
        owner.tentacles.append(self)

    def shock(self):
        self.connected.shocked(1)

    def __str__(self):
        id = self.id
        owner = self.owner
        connected = self.connected
        return f'Tentacle {id}: Octopus {owner.id} -> Octopus {connected.id}'


# In[7]:


class Beach:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.octopuses = []
        self.create_octopuses()
        self.connect_neighbours()

    def create_octopus(self, id):
        return Octopus(id=id)

    def create_octopuses(self):
        for i in range(0, self.width * self.height):
            octopus = self.create_octopus(id=i)
            self.octopuses.append(octopus)     

    def create_tentacle(self, id, owner, connected):
        return Tentacle(id=id, owner=owner, connected=connected)

    def connect_neighbours(self):
        width = self.width
        height = self.height

        def get_neighbours(x, y):
            neighbours = []
            neighbours.append((x - 1, y - 1))
            neighbours.append((x - 1, y))
            neighbours.append((x - 1, y + 1))
            neighbours.append((x, y - 1))
            neighbours.append((x, y + 1))
            neighbours.append((x + 1, y - 1))
            neighbours.append((x + 1, y))
            neighbours.append((x + 1, y + 1))
            return neighbours

        for i in range(0, width * height):
            octopus = self.octopuses[i]
            coors_neighbours = get_neighbours(i // height, i % width)
            tentacle_id = 0
            for x, y in coors_neighbours:
                try:
                    neighbour = self.get(x, y)
                    tentacle = self.create_tentacle(
                        id=tentacle_id, owner=octopus, connected=neighbour
                    )
                    tentacle_id += 1
                except:
                    continue

    def get(self, x, y,):
        width = self.width
        height = self.height
        if (0 <= x < height) and (0 <= y < width):
            return self.octopuses[x * width + y]
        else:
            raise Exception

    def detail(self):
        result = ''
        for octopus in self.octopuses:
            result += octopus.detail()
        return result

    def __str__(self):
        result = '\n'
        for x in range(0, self.height):
            for y in range(0, self.width):
                octopus = self.octopuses[x * self.width + y]
                result += '💡' if octopus.awake else '🐙'
            result += '\n'
        return result


# In[9]:


from random import shuffle

class Helicopter:

    @staticmethod
    def light(beach, where):
        shuffle(where)
        for x, y in where:
            octopus = beach.get(x, y)
            octopus.shocked(Octopus.shocks_threshold)


# In[11]:


class AllSleepingException(Exception):
    pass

class BeachWithSpreading(Beach):

    def __init__(self, width, height, shocks_threshold=3):
        super().__init__(width, height)
        Octopus.shocks_threshold = shocks_threshold

    def start(self, where):
        Helicopter.light(self, where)

    def print_start(self, show):
        if show:
            print('Start')
            print(self)

    def iteration(self):
        awake = [o for o in self.octopuses if o.awake]
        if len(awake) == 0:
            raise AllSleepingException
        for octopus in awake:
            for tentacle in octopus.tentacles:
                tentacle.shock()

    def print_iteration(self, show, i):
        if show:
            print(f'Iteration {i + 1}')
            print(self)

    def animate(self, where=None, iterations=10, show=True):
        if where != None:
            self.start(where)
        self.print_start(show)
        for i in range(0, iterations):
            try:
                self.iteration()
                self.print_iteration(show, i)
            except AllSleepingException:
                if show == True:
                    print('It looks like everyone is sleeping 😕')
                break


# In[15]:


class OctopusWithSmell(Octopus):

    smell_threshold = 20

    def __init__(self, id, environment):
        super().__init__(id)
        self.environment = environment

    def shocked(self, power=0):
        if (self.awake):
            return
        self.excitement += power
        if (self.excitement >= Octopus.shocks_threshold and
            self.environment.smell < OctopusWithSmell.smell_threshold):
            self.awake = True
            self.environment.smell += 1


# In[16]:


class BeachWithSmell(BeachWithSpreading):

    def __init__(self, width, height, shocks_threshold=5, smell_threshold=20):
        super().__init__(width, height, shocks_threshold)
        self.smell = 0
        OctopusWithSmell.smell_threshold = smell_threshold

    def create_octopus(self, id):
        return OctopusWithSmell(id=id, environment=self)

    def print_iteration(self, show, i):
        if show:
            print(f'Iteration {i + 1} - smell: {self.smell}')
            print(self)


# In[19]:


class TentacleWithSoreness(Tentacle):

    def __init__(self, id, owner, connected):
        super().__init__(id, owner, connected)
        self.soreness = 1

    def shock(self):
        if self.connected.awake:
            self.soreness += 1
        else:
            self.connected.shocked(self.soreness)
            
    def __str__(self):
        return super().__str__() + f': Soreness {self.soreness}'


# In[20]:


class BeachWithSoreness(BeachWithSmell):

    def __init__(self, width, height, shocks_threshold=50, smell_threshold=50):
        super().__init__(width, height, shocks_threshold, smell_threshold)

    def create_tentacle(self, id, owner, connected):
        return TentacleWithSoreness(id=id, owner=owner, connected=connected)

    def print_night(self):
        print()
        print("Night\n")
        for i in range(0, self.height):
            print("🌚" * self.width)
        print("\n")
            
    def night(self, show=False):
        for octopus in self.octopuses:
            if octopus.awake: self.smell -= 1
            octopus.awake = False
            octopus.excitement = 0
        if show: self.print_night()


# In[22]:


class OctopusWithTiredness(OctopusWithSmell):

    tiredness_threshold = 10
    recovery_threshold = 10

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self.tiredness = 0
        self.recovering = False
        self.recover_status = 0

    def tired(self):
        self.tiredness += 1
        if (self.tiredness >
            OctopusWithTiredness.tiredness_threshold):
            self.sleep(night=False)

    def recover(self):
        self.recover_status += 1
        if (self.recover_status >=
            OctopusWithTiredness.recovery_threshold):
            self.recovering = False
            self.recover_status = 0
            
    def shocked(self, power=0):
        if not self.recovering:
            super().shocked(power)

    def sleep(self, night=True):
        if self.awake: self.environment.smell -= 1
        self.awake = False
        self.excitement = 0
        self.tiredness = 0
        if night:
            self.recovering = False
            self.recover_status = 0
        else:
            self.recovering = True


# In[23]:


from random import shuffle

class BeachWithTiredness(BeachWithSoreness):

    def __init__(self, width, height, shocks_threshold=80, smell_threshold=50,
                 tiredness_threshold=5, recovery_threshold=5):
        super().__init__(width, height, shocks_threshold, smell_threshold)
        OctopusWithTiredness.tiredness_threshold = tiredness_threshold
        OctopusWithTiredness.recovery_threshold = recovery_threshold

    def create_octopus(self, id):
        return OctopusWithTiredness(id=id, environment=self)

    def iteration(self):
        awake = [o for o in self.octopuses if o.awake]
        if len(awake) == 0:
            raise AllSleepingException
        shuffle(awake)
        for octopus in awake:
            octopus.tired()
            for tentacle in octopus.tentacles:
                tentacle.shock()
        recovering = [o for o in self.octopuses if o.recovering]
        for octopus in recovering:
            octopus.recover()

    def night(self, show=False):
        for octopus in self.octopuses:
            octopus.sleep()
        if show: self.print_night()

# In[25]:


class OctopusWithListeners(OctopusWithTiredness):

    def __init__(self, id, environment):
        super().__init__(id, environment)
        self.listeners = []

    def attach_listener(self, listener):
        self.listeners.append(listener)

    def fire_listeners(self):
        for listener in self.listeners:
            listener.fire(self)

    def shocked(self, power=0):
        was_awake = self.awake
        super().shocked(power)
        is_awake = self.awake
        if (not was_awake and is_awake):
            self.fire_listeners()
            
    def tired(self):
        was_awake = self.awake
        super().tired()
        is_awake = self.awake
        if (was_awake and not is_awake):
            self.fire_listeners()


# In[26]:


class BeachWithListeners(BeachWithTiredness):

    def __init__(self, width, height, shocks_threshold=80,
                 smell_threshold=50, tiredness_threshold=5, recovery_threshold=5):
        super().__init__(width, height, shocks_threshold, smell_threshold, tiredness_threshold, recovery_threshold)
        self.listeners = set([])

    def create_octopus(self, id):
        return OctopusWithListeners(id=id, environment=self)

    def attach_listener(self, where, listener):
        self.listeners.add(listener)
        for x, y in where:
            octopus = self.get(x, y)
            octopus.attach_listener(listener)
    
    def night(self, show=False):
        super().night()
        for listener in self.listeners:
            listener.reset()