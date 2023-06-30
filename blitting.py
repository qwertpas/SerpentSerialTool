import sys
import matplotlib.pyplot as plt
import numpy as np


class BlitManager:
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for sub-classes of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist

            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()


class LivePlot():
    def __init__(self, labels, ymins, ymaxes, history=100):


        self.fig, axs = plt.subplots(nrows=len(labels))
        def on_close(event):
            sys.exit()
        self.fig.canvas.mpl_connect('close_event', on_close)

        self.num_lines = 0
        for i in range(len(labels)):
            self.num_lines += len(labels[i])

        self.x = np.linspace(0, history, history)
        self.data = np.zeros((self.num_lines, history))

        self.lines = []

        print(f"LivePlot: Created {self.num_lines} lines on {len(labels)} subplots")

        for i in range(len(labels)):
            axs[i].set_ylim(ymins[i], ymaxes[i])
            for j in range(len(labels[i])):
                (ln,) = axs[i].plot(self.x, self.data[len(self.lines)], 'o-', label=labels[i][j], markersize=1)
                self.lines.append(ln)
            axs[i].legend(loc='lower left')

        self.bm = BlitManager(self.fig.canvas, self.lines)
        self.labels = labels

        plt.show(block=False)
        plt.pause(.1)

    def plot(self, *new_data):
        new_data = np.array(new_data).flatten()

        assert len(new_data) == self.num_lines

        for i in range(len(new_data)):
            self.data[i] = np.roll(self.data[i], -1)
            self.data[i][-1] = new_data[i]
            self.lines[i].set_ydata(self.data[i])

        self.bm.update()


    def close(self):
        plt.close(self.fig)


if __name__ == "__main__":

    plt.style.use('bmh')

    lp = LivePlot(
        labels=(('a', 'b'), 'c'),
        ymins = (-1, -2),
        ymaxes = (1, 2),
        history=100
    )


    t = 0
    while t < 5:
        
        lp.plot(np.sin(t), np.cos(t), np.tan(t))
        plt.pause(0.02)
        t += 0.02

    lp.close()