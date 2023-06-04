import matplotlib.pyplot as plt

class Plotter:
    @staticmethod
    def plot_events(data, event_indices, event_labels):
        x_values = data[:, 0]
        y_values = data[:, 1]

        plt.plot(x_values, y_values)
        plt.scatter(x_values[event_indices], y_values[event_indices], c='r', label='Events')

        for index, label in zip(event_indices, event_labels):
            plt.annotate(label, (x_values[index], y_values[index]), label=label)
            
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Event Detection')
        plt.legend()
        plt.savefig('event_plot.png')
        plt.close()