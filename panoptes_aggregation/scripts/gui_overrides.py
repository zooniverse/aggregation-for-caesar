def pbar_override(progressbar):
    def update1(self, *args, **kwargs):
        progressbar.bar.ProgressBarMixinBase.update(self, *args, **kwargs)
        line = progressbar.bar.converters.to_unicode(self._format_line())
        print('R| ' + line, flush=True, end='')

    def finish(self, *args, **kwargs):
        try:
            self._finished
        except AttributeError:
            self._finished = False
        if self._finished:
            return
        end = kwargs.pop('end', '\n')
        progressbar.bar.ProgressBarMixinBase.finish(self, *args, **kwargs)
        if end:
            print(end, flush=True)
        self.fd.flush()

    progressbar.bar.DefaultFdMixin.update = update1
    progressbar.bar.DefaultFdMixin.finish = finish

    def update2(self, value=None):
        print(' ' * self.term_width, flush=True)
        progressbar.bar.utils.streams.flush()
        progressbar.bar.DefaultFdMixin.update(self, value=value)

    progressbar.bar.StdRedirectMixin.update = update2


def gui_override(gooey):
    def appendText(self, txt):
        """
        Append the text to the main TextCtrl.
        Note! Must be called from a Wx specific thread handler to avoid
        multi-threaded explosions (e.g. wx.CallAfter)
        """
        if txt.startswith('R| '):
            txt = txt[3:]
            self.textbox.Clear()
        self.textbox.AppendText(txt)

    gooey.gui.components.console.Console.appendText = appendText
